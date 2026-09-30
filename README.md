# Clip to PSD

[![Download for Windows](https://img.shields.io/badge/Download-for%20Windows-blue?style=for-the-badge)](https://github.com/Oreyou101/clip-to-psdv2/releases/latest/download/ClipToPSD_Setup.exe)
![Latest version](https://img.shields.io/github/v/release/Oreyou101/clip-to-psdv2)

Convert Clip Studio Paint `.clip` files to Photoshop `.psd` - no Clip Studio or Python needed.

![Screenshot](screenshot.png) 

## Why this project?

The original tool, [clip_to_psd](https://github.com/dobrokot/clip_to_psd) by dobrokot, is a great
converter, but it runs from the command line and needs Python installed. The goal of this project is
to make it **easy for everyone**, especially artists who are not used to programming:

- a simple **graphical window**: choose a file, choose where to save, click, done
- a normal **Windows installer** with a desktop shortcut
- **no Python and no commands** needed

> **Important:** The conversion engine (`clip_to_psd.py`) is **not my code**. It was written by
> [dobrokot](https://github.com/dobrokot/clip_to_psd) and is used here under the MIT License.
> I only added the graphical interface (`clip_converter.py`), the installer and the packaging scripts.
> All credit for the conversion itself goes to the original author.
> Please support the original project: https://github.com/dobrokot/clip_to_psd

## Use
1. Click the **Download for Windows** button above (or get `ClipToPSD_Setup.exe` from the Releases page) and run it.
2. Click Next, keep "Create a desktop shortcut" ticked, click Install.
3. Open **Clip to PSD** from the desktop, choose your `.clip` file, then choose where to save the `.psd`.

No administrator rights are needed. To remove it, use Windows Settings -> Apps.

Windows may show "Windows protected your PC" because the app is not code-signed.
Click **More info -> Run anyway**. The full source code is in this repository.

## Limits
Vector layers, tone, frame borders, 3D and animation data are not fully supported;
some effects (Color Balance, Posterize, Gradient Map) are not exported.
Your original file is never modified.

If something fails, the log is saved at `%LOCALAPPDATA%\ClipToPSD\last_conversion.log`.

## Notes
- Please convert only files you created or have permission to use.
- The program is provided "as is", without warranty. Keep a backup of your original files.
- This project is not affiliated with or endorsed by Celsys (Clip Studio Paint) or Adobe (Photoshop). Those names belong to their owners.

## Credits
- Conversion engine: [clip_to_psd](https://github.com/dobrokot/clip_to_psd) by dobrokot (MIT License).
- GUI and installer: Oreyou101.
