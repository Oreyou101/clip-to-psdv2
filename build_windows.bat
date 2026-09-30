@echo off
REM Run on Windows, in this folder. Needs Python 3.10+ from python.org.
REM For the Setup.exe installer, also install Inno Setup 6 (free): https://jrsoftware.org/isdl.php
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --windowed --name ClipToPSD --icon icon.ico --add-data "LICENSE;." --add-data "icon.ico;." clip_converter.py
if errorlevel 1 goto fail

set "ISCC="
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if "%ISCC%"=="" goto noinno
"%ISCC%" installer.iss
if errorlevel 1 goto fail
echo.
echo DONE. Give people this file:  Output\ClipToPSD_Setup.exe
goto end

:noinno
echo.
echo Program built in dist\ClipToPSD\ClipToPSD.exe
echo Inno Setup was not found, so no Setup.exe was created.
echo Install Inno Setup 6 from https://jrsoftware.org/isdl.php and run this file again.
goto end

:fail
echo.
echo Build failed - see the messages above.

:end
pause