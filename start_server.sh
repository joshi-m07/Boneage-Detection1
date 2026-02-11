# Quick Start for Bash/Linux
echo "================================================"
echo " Bone Age Estimation Backend - Quick Start"
echo "================================================"
echo

echo "[1/3] Initializing database..."
python -c "from database.db import init_db; init_db()"

echo
echo "[2/3] Starting API server..."
echo
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "MLflow UI: Run 'mlflow ui' in another terminal"
echo
echo "Press Ctrl+C to stop the server"
echo

python app.py
