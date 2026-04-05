$ProjectRoot = Get-Location
$PythonExe = Join-Path $ProjectRoot "venv\Scripts\python.exe"
$ScriptFile = "get_crypto_price.py"
$TaskName = "CryptoPriceMonitor"

if (-not (Test-Path $PythonExe)) {
    Write-Error "Error: python.exe not found in venv."
    exit 1
}

# 1. アクションの作成
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument $ScriptFile -WorkingDirectory $ProjectRoot.Path

# 2. 毎日のトリガーを作成 (09:00 開始)
$Trigger = New-ScheduledTaskTrigger -Daily -At 9:00am

# 3. 繰り返し設定の生成とコピー
# New-ScheduledTaskTrigger の -Once パラメータセットは繰り返し設定の生成をサポートしているため、
# それを利用して正しい Repetition オブジェクトを作成し、Daily トリガーに流用します。
$TempTrigger = New-ScheduledTaskTrigger -Once -At 9:00am -RepetitionInterval (New-TimeSpan -Hours 3) -RepetitionDuration (New-TimeSpan -Hours 14)
$Trigger.Repetition = $TempTrigger.Repetition

# 4. 既存タスクがあれば削除
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# 5. タスクの登録
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "Crypto Price Monitor Task" -User $env:USERNAME

Write-Host "--------------------------------------------------"
Write-Host "Task registered successfully."
Write-Host "Schedule: 09:00 - 23:00, every 3 hours."
Write-Host "--------------------------------------------------"
