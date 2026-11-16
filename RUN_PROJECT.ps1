$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Creating project virtual environment..." -ForegroundColor Red
    py -3.15 -m venv .venv
}

$python = ".\.venv\Scripts\python.exe"
Write-Host "Installing project requirements..." -ForegroundColor Red
& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt
Write-Host "Applying database migrations..." -ForegroundColor Red
& $python manage.py migrate
Write-Host "Loading Taza demo products, outlets and coupons..." -ForegroundColor Red
& $python manage.py seed_demo
Write-Host "Starting Taza Food Corner at http://127.0.0.1:8000/" -ForegroundColor Red
& $python manage.py runserver
