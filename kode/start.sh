#!/bin/bash
# QUICK START SCRIPT - Gempa Indonesia Visualization Project
# Jalankan: bash start.sh (Linux/Mac) atau start.bat (Windows)

echo "=================================================="
echo "🌍 Visualisasi Sebaran Gempa Bumi Indonesia"
echo "=================================================="
echo ""

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python found: $($PYTHON_CMD --version)"
echo ""

# Check if data files exist
echo "[1/3] Checking data files..."
if [ ! -f "data/katalog_gempa_clean.csv" ]; then
    echo "⚠️  Cleaned data not found. Running preprocessing..."
    cd analysis
    $PYTHON_CMD 1_data_preprocessing.py
    $PYTHON_CMD 2_anomaly_detection.py
    $PYTHON_CMD 3_data_conversion.py
    cd ..
fi
echo "✓ Data files ready"
echo ""

# Check if web data exists
echo "[2/3] Checking web data files..."
if [ ! -f "web/data/earthquakes_sample.geojson" ]; then
    echo "⚠️  Web data files not found. Regenerating..."
    cd analysis
    $PYTHON_CMD 3_data_conversion.py
    cd ..
fi
echo "✓ Web data files ready"
echo ""

# Start HTTP server
echo "[3/3] Starting web server..."
cd web
echo ""
echo "=================================================="
echo "✓ Server started successfully!"
echo "=================================================="
echo ""
echo "📍 Open your browser and go to:"
echo "   👉 http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
$PYTHON_CMD -m http.server 8000
