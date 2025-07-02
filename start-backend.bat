@echo off
echo Starting AI Comic Factory Backend...
echo.

cd backend

echo Creating virtual environment if it doesn't exist...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
echo Backend will be available at: http://localhost:8000
echo.
python main.py

pause 