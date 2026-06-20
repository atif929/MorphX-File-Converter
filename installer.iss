[Setup]
AppName=MorphX
AppVersion=1.1.0
AppPublisher=Atif
DefaultDirName={autopf}\MorphX
DefaultGroupName=MorphX
OutputDir=installer_output
OutputBaseFilename = MorphX_Setup_v1.1.0
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create Desktop Shortcut"; Flags: checkedonce
Name: "startmenu"; Description: "Add to Start Menu"; Flags: checkedonce

[Files]
Source: "dist\MorphX\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MorphX"; Filename: "{app}\MorphX.exe"
Name: "{commondesktop}\MorphX"; Filename: "{app}\MorphX.exe"; Tasks: desktopicon
Name: "{commonstartmenu}\MorphX"; Filename: "{app}\MorphX.exe"; Tasks: startmenu

[Run]
Filename: "{app}\MorphX.exe"; Description: "Launch MorphX"; Flags: nowait postinstall skipifsilent