@echo off
echo ========================================
echo 🚀 Starting All Services
echo ========================================
echo.

echo Starting Redis Server...
start "Redis Server" cmd /k "python start_redis.py"

timeout /t 3 /nobreak > nul

echo Starting Dramatiq Worker...
start "Dramatiq Worker" cmd /k "python start_dramatiq.py"

timeout /t 2 /nobreak > nul

echo Starting Backend Server...
start "Backend Server" cmd /k "python start_backend.py"

echo.
echo ========================================
echo ✅ All services started!
echo ========================================
echo.
echo Services running:
echo - Redis: redis://127.0.0.1:6379
echo - Backend: http://127.0.0.1:8000
echo - Dramatiq: Processing background tasks
echo.
echo Press any key to close this window...
pause > nul
