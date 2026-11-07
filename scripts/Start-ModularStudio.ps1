# Start-ModularStudio.ps1

Write-Host "Starting Modular Studio..." -ForegroundColor Cyan

# Check if Ollama is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -ErrorAction Stop
    Write-Host "[OK] Ollama is running." -ForegroundColor Green
} catch {
    Write-Host "[WAIT] Ollama is not running, starting it..." -ForegroundColor Yellow
    Start-Process "ollama" -ArgumentList "serve" -NoNewWindow
    Start-Sleep -Seconds 3
}

# Start Backend
Write-Host "Starting FastAPI Backend..." -ForegroundColor Cyan
Start-Process "uv" -ArgumentList "run uvicorn backend.main:app --reload --port 8000" -NoNewWindow

# Start Frontend
Write-Host "Starting Next.js Frontend..." -ForegroundColor Cyan
Set-Location "frontend"
Start-Process "npm" -ArgumentList "run dev" -NoNewWindow
Set-Location ".."

# Open Browser
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000/modular_studio"

Write-Host "Modular Studio Started!" -ForegroundColor Green
