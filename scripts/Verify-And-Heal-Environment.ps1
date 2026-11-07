# Verify-And-Heal-Environment.ps1

Write-Host "Verifying and Healing Environment..." -ForegroundColor Cyan

# Check Python
$pythonVer = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Python installed: $pythonVer" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Python 3.11+ is required but not found." -ForegroundColor Red
}

# Check Node
$nodeVer = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Node installed: $nodeVer" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Node.js is required but not found." -ForegroundColor Red
}

# Check UV
$uvVer = uv --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] uv installed: $uvVer" -ForegroundColor Green
} else {
    Write-Host "[FAIL] uv is required but not found." -ForegroundColor Red
}

# Check FFmpeg
$ffmpegVer = ffmpeg -version 2>&1 | Select-Object -First 1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] FFmpeg installed: $ffmpegVer" -ForegroundColor Green
} else {
    Write-Host "[FAIL] FFmpeg is required but not found." -ForegroundColor Red
}

# Check Manim
$manimVer = manim --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Manim installed: $manimVer" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Manim is required but not found." -ForegroundColor Red
}

# Check Blender CLI
$blenderVer = blender --version 2>&1 | Select-Object -First 1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Blender CLI installed: $blenderVer" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Blender CLI is required but not found." -ForegroundColor Red
}

# Check local Ollama
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -ErrorAction Stop
    Write-Host "[OK] Local Ollama is running." -ForegroundColor Green
} catch {
    Write-Host "[FAIL] Local Ollama is not running." -ForegroundColor Red
}

# Ensure .env exists
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[HEAL] Created .env from .env.example" -ForegroundColor Yellow
    } else {
        New-Item ".env" -ItemType File | Out-Null
        Write-Host "[HEAL] Created empty .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
}

Write-Host "Environment Check Complete." -ForegroundColor Cyan
