# Run as Administrator in PowerShell
# Registers the JPATE Triage Agent as a Windows Scheduled Task
$taskName = "JPATE Triage Agent"
$pythonPath = (Get-Command python).Source
$scriptPath = "C:\Users\jacks\JPATE\agent\agent.py"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptPath
$triggerLogin = New-ScheduledTaskTrigger -AtLogOn
$triggerRepeat = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 5) -Once -At (Get-Date)
$settings = New-ScheduledTaskSettingsSet -RestartOnIdle -RunOnlyIfNetworkAvailable

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $triggerLogin,$triggerRepeat `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Task '$taskName' registered."
Write-Host "To start immediately: Start-ScheduledTask -TaskName '$taskName'"
