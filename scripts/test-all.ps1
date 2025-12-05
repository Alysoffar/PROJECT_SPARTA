#!/usr/bin/env pwsh
# Test all services script

Write-Host "Testing SPARTA Services..." -ForegroundColor Cyan
Write-Host ""

$services = @(
    @{Name="Gateway"; Path="gateway"},
    @{Name="Orchestrator"; Path="orchestrator"},
    @{Name="Emulator"; Path="services\emulator"}
)

$allPassed = $true

foreach ($service in $services) {
    Write-Host "Testing $($service.Name)..." -ForegroundColor Yellow
    Push-Location $service.Path
    
    if (Test-Path "tests") {
        python -m pytest tests -v
        if ($LASTEXITCODE -ne 0) {
            $allPassed = $false
            Write-Host "✗ $($service.Name) tests failed" -ForegroundColor Red
        } else {
            Write-Host "✓ $($service.Name) tests passed" -ForegroundColor Green
        }
    } else {
        Write-Host "⚠ No tests found for $($service.Name)" -ForegroundColor DarkYellow
    }
    
    Pop-Location
    Write-Host ""
}

if ($allPassed) {
    Write-Host "All tests passed! ✓" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Some tests failed! ✗" -ForegroundColor Red
    exit 1
}
