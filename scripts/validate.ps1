# SPARTA System Validation Script

Write-Host "SPARTA System Validation" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

$passed = 0
$total = 0

# Check 1: Docker installed
Write-Host "1. Checking Docker Desktop..." -ForegroundColor Cyan
$total++
try {
    $null = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] Docker is installed" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "   [FAIL] Docker not found" -ForegroundColor Red
    }
} catch {
    Write-Host "   [FAIL] Docker not found" -ForegroundColor Red
}

# Check 2: Docker running
Write-Host "2. Checking Docker is running..." -ForegroundColor Cyan
$total++
try {
    $null = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] Docker Desktop is running" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "   [FAIL] Docker Desktop not running" -ForegroundColor Red
    }
} catch {
    Write-Host "   [FAIL] Cannot connect to Docker" -ForegroundColor Red
}

# Check 3: Containers running
Write-Host "3. Checking SPARTA containers..." -ForegroundColor Cyan
$total++
try {
    $containers = docker compose ps --format json 2>&1 | ConvertFrom-Json
    if ($containers) {
        $runningCount = ($containers | Where-Object { $_.State -eq "running" }).Count
        if ($runningCount -gt 0) {
            Write-Host "   [OK] $runningCount containers running" -ForegroundColor Green
            $passed++
        } else {
            Write-Host "   [FAIL] No containers running" -ForegroundColor Red
        }
    } else {
        Write-Host "   [FAIL] No containers found" -ForegroundColor Red
    }
} catch {
    Write-Host "   [FAIL] Cannot query containers" -ForegroundColor Red
}

# Check 4: Service health
Write-Host "4. Checking service health..." -ForegroundColor Cyan
$total++
$healthyServices = 0
$testServices = @("http://localhost:8000/health", "http://localhost:8001/health")

foreach ($url in $testServices) {
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $healthyServices++
        }
    } catch {
        # Service not ready
    }
}

if ($healthyServices -eq $testServices.Count) {
    Write-Host "   [OK] All core services responding" -ForegroundColor Green
    $passed++
} else {
    Write-Host "   [WARN] $healthyServices/$($testServices.Count) services responding" -ForegroundColor Yellow
}

# Check 5: Python installed
Write-Host "5. Checking Python environment..." -ForegroundColor Cyan
$total++
try {
    $null = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] Python is installed" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "   [FAIL] Python not found" -ForegroundColor Red
    }
} catch {
    Write-Host "   [FAIL] Python not found" -ForegroundColor Red
}

# Summary
Write-Host ""
Write-Host "Validation Summary" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Results: $passed/$total checks passed" -ForegroundColor $(if ($passed -eq $total) { "Green" } elseif ($passed -ge 3) { "Yellow" } else { "Red" })
Write-Host ""

if ($passed -eq $total) {
    Write-Host "[OK] System is fully operational!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  - Access frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "  - View API docs: http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  - Run tests: pytest tests\test_integration.py -v" -ForegroundColor White
} elseif ($passed -ge 3) {
    Write-Host "[WARN] System is partially operational" -ForegroundColor Yellow
    Write-Host "Some services may still be starting. Wait 1-2 minutes and try again." -ForegroundColor Gray
} else {
    Write-Host "[FAIL] System has issues" -ForegroundColor Red
    Write-Host ""
    Write-Host "Recommended actions:" -ForegroundColor Cyan
    Write-Host "  1. Ensure Docker Desktop is installed and running" -ForegroundColor White
    Write-Host "  2. Run: .\scripts\start.ps1" -ForegroundColor White
    Write-Host "  3. Check logs: docker compose logs -f" -ForegroundColor White
    Write-Host "  4. See TROUBLESHOOTING.md for help" -ForegroundColor White
}

Write-Host ""

if ($passed -eq $total) {
    exit 0
} else {
    exit 1
}
