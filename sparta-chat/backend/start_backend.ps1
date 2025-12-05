# Start SPARTA Chat Backend
Set-Location $PSScriptRoot
Write-Host "Starting backend from: $(Get-Location)" -ForegroundColor Green
python -m uvicorn main:app --host 0.0.0.0 --port 9000 --reload
