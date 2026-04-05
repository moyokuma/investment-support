$TaskName = "CryptoPriceMonitor"

# Check if the task exists anywhere in the Task Scheduler
$Task = Get-ScheduledTask | Where-Object { $_.TaskName -eq $TaskName }

if ($Task) {
    try {
        # Unregister the task
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
        Write-Host "--------------------------------------------------"
        Write-Host "Task '$TaskName' has been successfully removed."
        Write-Host "--------------------------------------------------"
    } catch {
        Write-Host "--------------------------------------------------"
        Write-Host "Error: Failed to remove task '$TaskName'."
        Write-Host $_.Exception.Message
        Write-Host "--------------------------------------------------"
    }
} else {
    Write-Host "--------------------------------------------------"
    Write-Host "Task '$TaskName' was not found."
    Write-Host "--------------------------------------------------"
}
