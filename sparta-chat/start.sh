#!/bin/bash
# SPARTA Chat Startup Script

echo "🚀 Starting SPARTA Chat System..."

# Start backend
echo "📡 Starting backend on port 9000..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 9000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend on port 8501..."
cd ../frontend
streamlit run app.py &
FRONTEND_PID=$!

echo ""
echo "✅ SPARTA Chat is running!"
echo "   Backend:  http://localhost:9000"
echo "   Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop..."

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
