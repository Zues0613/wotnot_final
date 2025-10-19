# PowerShell script to start all services
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Starting All Services" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Redis Server
Write-Host "Starting Redis Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python start_redis.py" -WindowStyle Normal

Start-Sleep -Seconds 3

# Start Dramatiq Worker
Write-Host "Starting Dramatiq Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python start_dramatiq.py" -WindowStyle Normal

Start-Sleep -Seconds 2

# Start Backend Server
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python start_backend.py" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services running:" -ForegroundColor White
Write-Host "- Redis: redis://127.0.0.1:6379" -ForegroundColor Red
Write-Host "- Backend: http://127.0.0.1:8000" -ForegroundColor Blue
Write-Host "- Dramatiq: Processing background tasks" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
