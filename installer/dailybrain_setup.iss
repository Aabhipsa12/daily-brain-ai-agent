[Setup]
AppName=Daily Brain
AppVersion=1.0.0
AppPublisher=Daily Brain
DefaultDirName={autopf}\DailyBrain
DefaultGroupName=Daily Brain
OutputDir=..\dist_installer
OutputBaseFilename=DailyBrainSetup
SetupIconFile=..\app.ico
UninstallDisplayIcon={app}\app.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: ".git*,.venv*,__pycache__*,dist*,dist_installer*,*.log"

[Icons]
Name: "{group}\Daily Brain"; Filename: "{app}\DailyBrain.bat"; IconFilename: "{app}\app.ico"
Name: "{group}\{cm:UninstallProgram,Daily Brain}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Daily Brain"; Filename: "{app}\DailyBrain.bat"; IconFilename: "{app}\app.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\DailyBrain.bat"; Description: "{cm:LaunchProgram,Daily Brain}"; Flags: shellexec postinstall nowait skipifsilent