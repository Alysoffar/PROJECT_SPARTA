# SPARTA Chat Startup Script (Windows)

Write-Host ' Starting SPARTA Chat System...' -ForegroundColor Green

# Start backend
Write-Host ' Starting backend on port 9000...' -ForegroundColor Cyan
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd backend; uvicorn main:app --host 0.0.0.0 --port 9000 --reload'

# Wait for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host ' Starting frontend on port 8501...' -ForegroundColor Cyan
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd frontend; streamlit run app.py'

Write-Host ''
Write-Host ' SPARTA Chat is running!' -ForegroundColor Green
Write-Host '   Backend:  http://localhost:9000' -ForegroundColor Yellow
Write-Host '   Frontend: http://localhost:8501' -ForegroundColor Yellow
Write-Host ''
Write-Host 'Close the terminal windows to stop the services.' -ForegroundColor Gray
