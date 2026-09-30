; Inno Setup script - builds ClipToPSD_Setup.exe
; Run AFTER PyInstaller has created dist\ClipToPSD

#define MyAppName "Clip to PSD"
#define MyAppVersion "1.0"
#define MyAppExe "ClipToPSD.exe"

[Setup]
AppId={{6F0B7B52-3C1D-4E58-9A2B-5D1C0E7A4F31}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\ClipToPSD
DefaultGroupName={#MyAppName}
; Per-user install: no administrator password needed
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=Output
OutputBaseFilename=ClipToPSD_Setup
LicenseFile=LICENSE
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\icon.ico
ArchitecturesInstallIn64BitMode=x64compatible

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Shortcuts:"

[Files]
Source: "dist\ClipToPSD\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
[Run]
Filename: "{app}\{#MyAppExe}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
