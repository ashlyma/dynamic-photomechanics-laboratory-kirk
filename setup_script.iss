[Setup]
AppName=YourApp
AppVersion=0.1
DefaultDirName={pf}\YourApp
DefaultGroupName=YourApp
OutputBaseFilename=YourAppInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "build\exe.win-amd64-3.x\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\YourApp"; Filename: "{app}\run_streamlit.exe"
Name: "{userdesktop}\YourApp"; Filename: "{app}\run_streamlit.exe"

[Run]
Filename: "{app}\run_streamlit.exe"; Description: "Launch YourApp"; Flags: nowait postinstall skipifsilent
