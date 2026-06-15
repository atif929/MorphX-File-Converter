[Setup]
AppName=FileConverter
AppVersion=1.0.0
AppPublisher=Atif
DefaultDirName={autopf}\FileConverter
DefaultGroupName=FileConverter
OutputDir=installer_output
OutputBaseFilename=FileConverter_Setup_v1.0.0
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\FileConverter\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FileConverter"; Filename: "{app}\FileConverter.exe"
Name: "{group}\Uninstall FileConverter"; Filename: "{uninstallexe}"
Name: "{commondesktop}\FileConverter"; Filename: "{app}\FileConverter.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FileConverter.exe"; Description: "Launch FileConverter"; Flags: nowait postinstall skipifsilent