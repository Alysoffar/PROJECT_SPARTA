# Quick start script for local development

Write-Host "SPARTA Quick Start" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

# Function to find Docker executable
function Find-Docker {
    # Common Docker Desktop installation paths
    $dockerPaths = @(
        "C:\Program Files\Docker\Docker\resources\bin\docker.exe",
        "C:\Program Files\Docker\Docker\Docker Desktop.exe",
        "$env:ProgramFiles\Docker\Docker\resources\bin\docker.exe",
        "$env:LOCALAPPDATA\Programs\Docker\Docker\resources\bin\docker.exe"
    )
    
    # First try to find docker in PATH
    $dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
    if ($dockerCmd) {
        return $dockerCmd.Source
    }
    
    # Search in common locations
    foreach ($path in $dockerPaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    
    return $null
}

# Function to check if Docker Desktop is running
function Test-DockerRunning {
    try {
        $null = & docker ps 2>&1
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Function to start Docker Desktop
function Start-DockerDesktop {
    Write-Host "Docker Desktop is not running. Attempting to start..." -ForegroundColor Yellow
    
    $dockerDesktopPaths = @(
        "C:\Program Files\Docker\Docker\Docker Desktop.exe",
        "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
    )
    
    foreach ($path in $dockerDesktopPaths) {
        if (Test-Path $path) {
            Write-Host "Starting Docker Desktop from: $path" -ForegroundColor Cyan
            Start-Process -FilePath $path
            
            # Wait for Docker to start (max 60 seconds)
            Write-Host "Waiting for Docker Desktop to start" -NoNewline
            $maxWait = 60
            $waited = 0
            while (-not (Test-DockerRunning) -and $waited -lt $maxWait) {
                Write-Host "." -NoNewline
                Start-Sleep -Seconds 2
                $waited += 2
            }
            Write-Host ""
            
            if (Test-DockerRunning) {
                Write-Host "[OK] Docker Desktop started successfully!" -ForegroundColor Green
                return $true
            } else {
                Write-Host "[FAIL] Docker Desktop failed to start in time" -ForegroundColor Red
                return $false
            }
        }
    }
    
    Write-Host "[FAIL] Docker Desktop executable not found" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    return $false
}

# Find Docker
$dockerPath = Find-Docker
if (-not $dockerPath) {
    Write-Host "[FAIL] Docker not found in PATH or common locations" -ForegroundColor Red
    Write-Host "Please ensure Docker Desktop is installed" -ForegroundColor Yellow
    Write-Host "Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
    exit 1
}

Write-Host "[OK] Docker found: $dockerPath" -ForegroundColor Green

# Add Docker to PATH for this session if needed
$dockerDir = Split-Path $dockerPath -Parent
if ($env:PATH -notlike "*$dockerDir*") {
    $env:PATH = "$dockerDir;$env:PATH"
}

# Check if Docker Desktop is running
if (-not (Test-DockerRunning)) {
    if (-not (Start-DockerDesktop)) {
        Write-Host "[FAIL] Cannot proceed without Docker Desktop running" -ForegroundColor Red
        exit 1
    }
}

Write-Host "[OK] Docker Desktop is running" -ForegroundColor Green
Write-Host ""

# Stop any existing containers
Write-Host "Stopping any existing SPARTA containers..." -ForegroundColor Yellow
try {
    docker compose down 2>&1 | Out-Null
} catch {
    Write-Host "No existing containers to stop" -ForegroundColor Gray
}

Write-Host "Starting services with Docker Compose..." -ForegroundColor Yellow
Write-Host ""

# Use 'docker compose' (v2 syntax) instead of 'docker-compose'
try {
    docker compose up -d --build
    if ($LASTEXITCODE -ne 0) {
        throw "Docker compose failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Host "[FAIL] Failed to start services: $_" -ForegroundColor Red
    Write-Host "Attempting with docker-compose (v1 syntax)..." -ForegroundColor Yellow
    docker-compose up -d --build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] Both docker compose commands failed" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Waiting for services to become healthy..." -ForegroundColor Yellow

# Function to check if a service is healthy
function Test-ServiceHealth {
    param(
        [string]$Url,
        [string]$ServiceName
    )
    
    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec 2 -ErrorAction SilentlyContinue
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# Wait for critical services with progress indicator
$services = @(
    @{Name="Gateway"; Url="http://localhost:8000/health"},
    @{Name="Orchestrator"; Url="http://localhost:8001/health"}
)

$maxWait = 120  # 2 minutes max wait
$waited = 0
$allHealthy = $false

Write-Host "Checking service health" -NoNewline
while (-not $allHealthy -and $waited -lt $maxWait) {
    Write-Host "." -NoNewline
    Start-Sleep -Seconds 3
    $waited += 3
    
    $healthyCount = 0
    foreach ($service in $services) {
        if (Test-ServiceHealth -Url $service.Url -ServiceName $service.Name) {
            $healthyCount++
        }
    }
    
    if ($healthyCount -eq $services.Count) {
        $allHealthy = $true
    }
}

Write-Host ""
Write-Host ""

if ($allHealthy) {
    Write-Host "[OK] All core services are healthy!" -ForegroundColor Green
} else {
    Write-Host "[WARN] Services are starting but may not be fully ready yet" -ForegroundColor Yellow
    Write-Host "This is normal - services may take up to 2 minutes to fully initialize" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Services Status:" -ForegroundColor Cyan

# Check individual service status
$allServices = @(
    @{Name="Gateway"; Url="http://localhost:8000/health"},
    @{Name="Orchestrator"; Url="http://localhost:8001/health"},
    @{Name="NLP Agent"; Url="http://localhost:8010/health"},
    @{Name="Synthesis Agent"; Url="http://localhost:8011/health"},
    @{Name="Emulator"; Url="http://localhost:8020/health"},
    @{Name="RTL Generator"; Url="http://localhost:8021/health"}
)

foreach ($service in $allServices) {
    if (Test-ServiceHealth -Url $service.Url -ServiceName $service.Name) {
        Write-Host "  [OK] $($service.Name)" -ForegroundColor Green
    } else {
        Write-Host "  [WAIT] $($service.Name) (starting...)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Access Points:" -ForegroundColor Cyan
Write-Host "  Frontend:     http://localhost:3000" -ForegroundColor White
Write-Host "  API Gateway:  http://localhost:8000" -ForegroundColor White
Write-Host "  Orchestrator: http://localhost:8001" -ForegroundColor White
Write-Host "  Swagger Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  View logs:    docker compose logs -f" -ForegroundColor White
Write-Host "  Stop all:     docker compose down" -ForegroundColor White
Write-Host "  Restart:      docker compose restart" -ForegroundColor White
Write-Host "  Check status: docker compose ps" -ForegroundColor White
Write-Host ""
Write-Host "[OK] SPARTA is ready!" -ForegroundColor Green
Write-Host ""
