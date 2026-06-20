@echo off
REM QUICK START SCRIPT - Gempa Indonesia Visualization Project
REM For Windows: Double-click this file or run from CMD

echo ==================================================
echo 🌍 Visualisasi Sebaran Gempa Bumi Indonesia
echo ==================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo ✓ Python found: %PYTHON_VER%
echo.

REM Check data files
echo [1/3] Checking data files...
if not exist "data\katalog_gempa_clean.csv" (
    echo ⚠️  Cleaned data not found. Running preprocessing...
    cd analysis
    python 1_data_preprocessing.py
    python 2_anomaly_detection.py
    python 3_data_conversion.py
    cd ..
)
echo ✓ Data files ready
echo.

REM Check web data
echo [2/3] Checking web data files...
if not exist "web\data\earthquakes_sample.geojson" (
    echo ⚠️  Web data files not found. Regenerating...
    cd analysis
    python 3_data_conversion.py
    cd ..
)
echo ✓ Web data files ready
echo.

REM Start server
echo [3/3] Starting web server...
cd web
echo.
echo ==================================================
echo ✓ Server started successfully!
echo ==================================================
echo.
echo 📍 Open your browser and go to:
echo    👉 http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
python -m http.server 8000

pause
