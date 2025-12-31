@echo off
echo ============================================================
echo 🚌 PeakMapPH Backend Server
echo ============================================================
echo 📡 Starting server on http://localhost:8000
echo 📖 API Documentation: http://localhost:8000/docs
echo 🔄 Auto-reload: Enabled
echo ============================================================
echo.
cd /d "%~dp0"
python -m uvicorn main:app --reload --port 8000
pause
