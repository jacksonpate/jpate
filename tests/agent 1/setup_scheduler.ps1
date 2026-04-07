# Run as Administrator in PowerShell
# Registers the JPATE Triage Agent as a Windows Scheduled Task
$taskName = "JPATE Triage Agent"
$pythonPath = (Get-Command python).Source
$workDir = "C:\Users\jacks\JPATE"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "-m agent.agent" -WorkingDirectory $workDir
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
