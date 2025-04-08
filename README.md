# Student Grade Management System

A web application for managing student grades, calculating averages, and displaying classifications.

## Features

- Display student information with grades
- Calculate and display average grades for each student
- Classify students based on their grades:
  - Distinction (70%+)
  - Merit (60%+)
  - Pass (40%+)
  - Fail (<40%)
- Filter students by classification
- View detailed statistics and visualizations

## Tech Stack

### Backend
- FastAPI (Python)
- SQLAlchemy (ORM)
- SQLite (Database)

### Frontend
- React (TypeScript)
- Tailwind CSS (Styling)
- React Router (Navigation)
- Axios (API Communication)

## Project Structure

```
tf_student_app/
├── backend/
│   ├── database.py      # Database connection and session
│   ├── models.py        # SQLAlchemy models
│   ├── routes.py        # API endpoints
│   ├── schemas.py       # Pydantic schemas
│   ├── sample_data.py   # Script to populate the database with sample data
│   └── main.py          # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   ├── App.tsx      # Main application component
│   │   └── main.tsx     # Entry point
│   ├── package.json     # Dependencies
│   └── tailwind.config.js # Tailwind configuration
└── README.md            # Documentation
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Seed the database with sample data:
   ```
   python sample_data.py
   ```

4. Run the backend server:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

## API Endpoints

### Students
- `GET /students/` - Get all students with average grades and classifications
- `GET /students/{student_id}` - Get student details with average grade and classification
- `GET /students/{student_id}/grades` - Get all grades for a specific student
- `POST /students/` - Create a new student

### Modules
- `GET /modules/` - Get all modules
- `GET /modules/{module_id}` - Get module details
- `POST /modules/` - Create a new module

### Tutors
- `GET /tutors/` - Get all tutors
- `GET /tutors/{tutor_id}` - Get tutor details
- `POST /tutors/` - Create a new tutor

### Grades
- `POST /grades/` - Create a new grade

## Sample Data

The application includes sample data for 10 students with various grades and classifications:
- 3 students with Distinction (70%+)
- 3 students with Merit (60%+)
- 2 students with Pass (40%+)
- 2 students with Fail (<40%)

## License

MIT 