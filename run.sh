#!/bin/bash

# Start the backend server
echo "Starting backend server..."
cd backend
python sample_data.py
uvicorn main:app --reload &
BACKEND_PID=$!

# Start the frontend server
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 