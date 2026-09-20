$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$StartMenuPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Programs)

$TargetDir = "D:\Daily-brain"
$TargetBat = Join-Path $TargetDir "DailyBrain.bat"
$IconFile = Join-Path $TargetDir "app.ico"

# 1. Create Desktop Shortcut
$ShortcutDesktop = $WshShell.CreateShortcut((Join-Path $DesktopPath "Daily Brain.lnk"))
$ShortcutDesktop.TargetPath = $TargetBat
$ShortcutDesktop.WorkingDirectory = $TargetDir
$ShortcutDesktop.IconLocation = "$IconFile, 0"
$ShortcutDesktop.Description = "Daily Brain - AI-Powered Task Management Agent"
$ShortcutDesktop.Save()

# 2. Create Start Menu Shortcut
$ShortcutStart = $WshShell.CreateShortcut((Join-Path $StartMenuPath "Daily Brain.lnk"))
$ShortcutStart.TargetPath = $TargetBat
$ShortcutStart.WorkingDirectory = $TargetDir
$ShortcutStart.IconLocation = "$IconFile, 0"
$ShortcutStart.Description = "Daily Brain - AI-Powered Task Management Agent"
$ShortcutStart.Save()

Write-Host "Daily Brain Desktop and Start Menu Shortcuts created successfully with official App Icon!"