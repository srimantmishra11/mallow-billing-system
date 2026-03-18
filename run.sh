#!/bin/bash
 
echo "============================================================"
echo "  BILLING SYSTEM - Setup and Run"
echo "============================================================"
echo ""
 
echo "[1/4] Creating virtual environment..."
python3 -m venv venv
 
echo "[2/4] Activating virtual environment..."
source venv/bin/activate
 
echo "[3/4] Installing dependencies..."
pip install -r requirements.txt
 
echo "[4/4] Initializing database..."
python scripts/seed_data.py
 
echo ""
echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
echo "Starting server..."
echo "Visit: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --port 8000