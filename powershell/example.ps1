Write-Output 'PowerShell automation sample started.'
Get-Date
Get-Process | Select-Object -First 5 | Format-Table -AutoSize
Write-Output 'PowerShell automation sample completed.'
