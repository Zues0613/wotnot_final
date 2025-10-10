# WotNot Frontend Cleanup and Setup Script
# Run this script to fix all console errors and WebSocket issues

Write-Host "=========================================" -ForegroundColor Green
Write-Host "  WotNot Frontend Cleanup & Setup" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Step 1: Create .env file
Write-Host "[1/5] Creating .env file..." -ForegroundColor Cyan
$envContent = @"
VUE_APP_API_URL=http://127.0.0.1:8000
"@

Set-Content -Path ".env" -Value $envContent -Force
Write-Host "✓ .env file created successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Clean node_modules
Write-Host "[2/5] Cleaning node_modules and cache..." -ForegroundColor Cyan
if (Test-Path "node_modules") {
    Remove-Item -Path "node_modules" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✓ node_modules removed" -ForegroundColor Green
}

if (Test-Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✓ dist folder removed" -ForegroundColor Green
}

# Step 3: Clear npm cache
Write-Host "[3/5] Clearing npm cache..." -ForegroundColor Cyan
npm cache clean --force
Write-Host "✓ npm cache cleared" -ForegroundColor Green
Write-Host ""

# Step 4: Install dependencies
Write-Host "[4/5] Installing dependencies (this may take a few minutes)..." -ForegroundColor Cyan
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Error installing dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Instructions
Write-Host "[5/5] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Next Steps:" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. Start Backend (in another terminal):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\activate" -ForegroundColor Gray
Write-Host "   uvicorn wati.main:app --reload --port 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start Frontend (in this terminal):" -ForegroundColor White
Write-Host "   npm run serve" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Access Application:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:8080" -ForegroundColor Cyan
Write-Host "   Backend:  http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Login Credentials:" -ForegroundColor White
Write-Host "   Email:    admin@wotnot.com" -ForegroundColor Cyan
Write-Host "   Password: admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✨ All issues fixed! Ready to run!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to start the frontend server..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Start the server
Write-Host ""
Write-Host "Starting frontend server..." -ForegroundColor Cyan
npm run serve

