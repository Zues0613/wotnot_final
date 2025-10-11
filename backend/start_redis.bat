@echo off
REM Redis Startup Script for WotNot Backend
REM This script starts Redis server in the background

echo Starting Redis server...
start /MIN "" "%USERPROFILE%\Redis\redis-server.exe" "%USERPROFILE%\Redis\redis.windows.conf"

timeout /t 3 /nobreak >nul

echo Checking Redis connection...
"%USERPROFILE%\Redis\redis-cli.exe" ping

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Redis is running successfully on localhost:6379
    echo.
    echo You can now start the Dramatiq worker:
    echo   dramatiq wati.services.tasks
    echo.
) else (
    echo ✗ Redis failed to start
    echo Please check the Redis window for errors
)

pause

