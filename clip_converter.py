"""
Clip to PSD - simple desktop app.

Graphical front end for clip_to_psd.py (by dobrokot, MIT license).
It calls the converter directly (no subprocess), so it also works
when packaged into a single .exe with PyInstaller.
"""
import io
import logging
import os
import queue
import sys
import threading
import traceback

APP_NAME = "Clip to PSD"
APP_VERSION = "1.0"


def _safe_std_streams():
    # A windowed (no console) exe has sys.stdout / sys.stderr = None.
    # Some code writes to them, so give them a harmless target.
    if sys.stdout is None:
        sys.stdout = io.StringIO()
    if sys.stderr is None:
        sys.stderr = io.StringIO()


def _log_file_path():
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    folder = os.path.join(base, "ClipToPSD")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "last_conversion.log")


def convert_clip_to_psd(input_path, output_path):
    """Convert one file. Returns (ok, log_text)."""
    _safe_std_streams()
    import clip_to_psd  # imported here so PyInstaller bundles it

    buffer = io.StringIO()
    handler = logging.StreamHandler(buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root = logging.getLogger()
    old_level = root.level
    root.addHandler(handler)
    root.setLevel(logging.INFO)

    old_argv = sys.argv
    sqlite_tmp = os.path.splitext(output_path)[0] + ".sqlite"
    ok = False
    try:
        sys.argv = ["clip_to_psd", input_path, "-o", output_path]
        clip_to_psd.main()
        ok = os.path.isfile(output_path)
    except SystemExit as e:
        ok = (e.code in (0, None)) and os.path.isfile(output_path)
    except Exception:
        buffer.write("\n" + traceback.format_exc())
    finally:
        sys.argv = old_argv
        root.removeHandler(handler)
        root.setLevel(old_level)
        # remove the temporary database if the converter left it behind
        if os.path.isfile(sqlite_tmp):
            try:
                os.remove(sqlite_tmp)
            except OSError:
                pass
        # do not leave a half-written PSD after a failure
        if not ok and os.path.isfile(output_path):
            try:
                os.remove(output_path)
            except OSError:
                pass

    text = buffer.getvalue()
    try:
        with open(_log_file_path(), "w", encoding="utf-8") as f:
            f.write(text)
    except OSError:
        pass
    return ok, text


def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.title(f"{APP_NAME} {APP_VERSION}")
    try:
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        root.iconbitmap(os.path.join(base, "icon.ico"))
    except Exception:
        pass
    root.geometry("440x360")
    root.resizable(False, False)
    root.configure(bg="#1a1a2e")

    results = queue.Queue()
    busy = {"value": False}

    def start():
        if busy["value"]:
            return
        in_path = filedialog.askopenfilename(
            title="اختر ملف Clip Studio Paint / Choose a .clip file",
            filetypes=[("Clip Studio Files", "*.clip")],
        )
        if not in_path:
            return
        default_name = os.path.splitext(os.path.basename(in_path))[0] + ".psd"
        out_path = filedialog.asksaveasfilename(
            title="احفظ ملف PSD / Save PSD as",
            initialdir=os.path.dirname(in_path),
            initialfile=default_name,
            defaultextension=".psd",
            filetypes=[("Photoshop", "*.psd")],
        )
        if not out_path:
            return
        if os.path.abspath(out_path) == os.path.abspath(in_path):
            messagebox.showerror("خطأ / Error", "Output must be a different file.")
            return

        busy["value"] = True
        btn.config(state="disabled")
        status.config(text="⏳ جاري التحويل... / Converting...", fg="#f0a500")

        def worker():
            ok, log = convert_clip_to_psd(in_path, out_path)
            results.put((ok, out_path, log))

        threading.Thread(target=worker, daemon=True).start()
        poll()

    def poll():
        try:
            ok, out_path, log = results.get_nowait()
        except queue.Empty:
            root.after(150, poll)
            return
        busy["value"] = False
        btn.config(state="normal")
        if ok:
            status.config(text="✅ تم التحويل بنجاح! / Done!", fg="#00e676")
            if messagebox.askyesno(
                "تم! / Done",
                f"Saved:\n{out_path}\n\nOpen the folder?\nفتح المجلد؟",
            ):
                try:
                    os.startfile(os.path.dirname(out_path))  # Windows
                except AttributeError:
                    pass
        else:
            status.config(text="❌ حدث خطأ! / Failed", fg="#ff5252")
            tail = "\n".join(log.strip().splitlines()[-12:])
            messagebox.showerror(
                "خطأ / Error",
                f"Conversion failed.\n\n{tail}\n\nFull log:\n{_log_file_path()}",
            )

    header = tk.Frame(root, bg="#16213e", pady=15)
    header.pack(fill="x")
    tk.Label(header, text="🎨", font=("Segoe UI Emoji", 32), bg="#16213e").pack()
    tk.Label(header, text="Clip Studio → Photoshop", font=("Segoe UI", 13, "bold"),
             bg="#16213e", fg="#e0e0e0").pack()
    tk.Label(header, text="حوّل ملفاتك بضغطة واحدة", font=("Segoe UI", 9),
             bg="#16213e", fg="#7986cb").pack(pady=(2, 0))
    tk.Frame(root, bg="#7986cb", height=2).pack(fill="x")

    body = tk.Frame(root, bg="#1a1a2e", pady=25)
    body.pack(fill="both", expand=True)
    tk.Label(body, text="اختر ملف .clip ثم مكان حفظ ملف .psd\nChoose a .clip file, then where to save the .psd",
             font=("Segoe UI", 10), bg="#1a1a2e", fg="#90a4ae",
             justify="center").pack(pady=(0, 18))
    btn = tk.Button(body, text="📂  اختر ملف .clip / Choose file",
                    font=("Segoe UI", 11, "bold"), bg="#7986cb", fg="white",
                    activebackground="#5c6bc0", activeforeground="white",
                    relief="flat", padx=25, pady=10, cursor="hand2", command=start)
    btn.pack()
    status = tk.Label(body, text="في انتظار الملف... / Waiting for a file...",
                      font=("Segoe UI", 9), bg="#1a1a2e", fg="#546e7a")
    status.pack(pady=(15, 0))

    tk.Label(root, text="Based on clip_to_psd by dobrokot (MIT)  •  GUI by Oreyou101",
             font=("Segoe UI", 7), bg="#1a1a2e", fg="#607d8b").pack(pady=(0, 8))

    root.eval("tk::PlaceWindow . center")
    root.mainloop()


if __name__ == "__main__":
    _safe_std_streams()
    run_gui()
