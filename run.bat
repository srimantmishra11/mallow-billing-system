@echo off
echo ============================================================
echo  BILLING SYSTEM - Setup and Run
echo ============================================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
 
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
 
echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
 
echo [4/4] Initializing database...
python scripts\seed_data.py
if errorlevel 1 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)
 
echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo Starting server...
echo Visit: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
uvicorn app.main:app --reload --port 8000
 
pause