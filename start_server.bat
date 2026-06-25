@echo off
echo ======================================
echo   INTEGRATY - AI Monitoring System
echo ======================================
echo.
echo Starting backend server...
echo Server will be available at http://localhost:8080
echo API docs at http://localhost:8080/docs
echo.
cd backend
python -m integraty.main
pause
