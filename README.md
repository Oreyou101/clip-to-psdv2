# Clip to PSD

Convert Clip Studio Paint `.clip` files to Photoshop `.psd` - no Clip Studio, Python or install needed.

## Use
1. Download `ClipToPSD_Setup.exe` from the Releases page and run it.
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
Conversion engine: [clip_to_psd](https://github.com/dobrokot/clip_to_psd) by dobrokot (MIT License).
GUI and installer by Oreyou101.