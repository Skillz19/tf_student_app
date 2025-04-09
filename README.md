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

### Infrastructure
- Docker
- Docker Compose

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
├── Dockerfile           # Backend Docker configuration
├── frontend.Dockerfile  # Frontend Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── .dockerignore        # Docker ignore file
└── README.md            # Documentation
```

## Getting Started

### Option 1: Docker Setup (Recommended)

1. Make sure you have Docker and Docker Compose installed on your machine.

2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

3. The application will be available at:
   - Frontend: http://127.0.0.1:5173
   - Backend API: http://127.0.0.1:8000

4. To stop the containers:
   ```bash
   docker-compose down
   ```

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Seed the database with sample data:
   ```bash
   python sample_data.py
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://127.0.0.1:5173`

### Convenience Script for Manual Setup (Mac/Linux/WSL2)

For users on Mac, Linux, or WSL2 who have completed the manual setup (Option 2), there's a convenience script `run.sh` that can start both the backend and frontend services with a single command:

1. Make the script executable:
   ```bash
   chmod +x run.sh
   ```

2. Run the script:
   ```bash
   ./run.sh
   ```

This script will:
- Start the backend server
- Start the frontend development server

To stop the services, press `Ctrl+C` in the terminal where the script is running.

> **Note**: This script is only applicable if you've completed the manual setup (Option 2). It does not work with the Docker setup (Option 1) as Docker runs in isolated containers. The script assumes you have already installed all dependencies and set up the project.

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
- `GET /grades/module/{module_id}` - Get all grades for a specific module
- `PUT /grades/{student_id}/{module_id}` - Update a grade for a student in a specific module

## Development

### Docker Commands

- View running containers:
  ```bash
  docker ps
  ```

- View container logs:
  ```bash
  docker-compose logs -f
  ```

- Rebuild and restart a specific service:
  ```bash
  docker-compose up --build <service_name>
  ```

- Stop all containers:
  ```bash
  docker-compose down
  ```

### Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: SQLite database URL (default: sqlite:///./students.db)
- `VITE_API_URL`: Backend API URL (default: http://127.0.0.1:8000)

## API Documentation

FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc. These are available at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The documentation includes:
- All available endpoints
- Request and response schemas
- Example requests and responses
- Error codes and descriptions

You can use these interactive documentation pages to explore the API and test endpoints directly from your browser.

## Testing

The application includes a comprehensive test suite for the backend:

### Backend Tests

#### Unit Tests
Located in `backend/tests/unit_tests/`:
- `test_students.py`: Tests for student model and business logic
- `test_tutors.py`: Tests for tutor model and business logic
- `test_modules.py`: Tests for module model and business logic
- `test_grades.py`: Tests for grade model and business logic

Run unit tests with:
```bash
cd backend
pytest tests/unit_tests
```

#### Integration Tests
Located in `backend/tests/integration_tests/`:
- `test_student_api.py`: Tests for student API endpoints
- `test_tutor_api.py`: Tests for tutor API endpoints
- `test_module_api.py`: Tests for module API endpoints

Run integration tests with:
```bash
cd backend
pytest tests/integration_tests
```

Run all tests with:
```bash
cd backend
pytest
```

### Frontend Tests

The frontend uses Vitest and React Testing Library for testing. The test setup includes:

- Unit tests for React components
- Mock service worker (MSW) for API mocking
- Jest DOM for DOM testing utilities

Run frontend tests with:
```bash
cd frontend
npm test
```

The frontend also uses ESLint for code quality checks. Run the linter with:
```bash
cd frontend
npm run lint
```

## License

This project is licensed under the MIT License.

## Design Choices and Justification

### Tech Stack Selection

#### Backend
- **FastAPI**: Chosen for its high performance, automatic API documentation, and type checking with Pydantic. It provides excellent developer experience with minimal boilerplate code.
- **SQLAlchemy**: Selected for its powerful ORM capabilities, database abstraction, and flexibility in query building. It allows for easy database migrations and complex queries.
- **SQLite**: Used for simplicity and ease of setup. While not suitable for high-scale production, it's perfect for a technical test as it requires no additional setup and demonstrates database concepts effectively.

#### Frontend
- **React with TypeScript**: Chosen for its component-based architecture, strong typing, and extensive ecosystem. TypeScript provides better developer experience and catches errors early.
- **Tailwind CSS**: Selected for rapid UI development and consistent styling. It eliminates the need for custom CSS files and provides a utility-first approach to styling.
- **Vite**: Used for its fast development server and optimized build process. It significantly improves development experience with hot module replacement.

### Architecture Decisions

#### API Design
- RESTful API design with clear resource-based endpoints
- Consistent response formats for better client-side handling
- Proper HTTP status codes for different scenarios
- API versioning for future compatibility

#### Database Design
- Normalized database schema to prevent data redundancy
- Clear relationships between entities (students, tutors, modules, grades)
- Appropriate indexing for performance optimization
- Use of foreign keys for data integrity

#### Frontend Architecture
- Component-based architecture for reusability and maintainability
- Separation of concerns (components, services, utilities)
- Centralized state management for data consistency
- Responsive design for various screen sizes

### Testing Strategy
- Unit tests for individual components and business logic
- Integration tests for API endpoints
- Mock service worker for frontend API testing
- ESLint for code quality and consistency

### Development Workflow
- Docker for consistent development environments
- Git hooks for code quality checks
- Automated testing in the development process
- Clear documentation for setup and usage

### Future Considerations
- Authentication and authorization for secure access
- Caching for improved performance
- Database migrations for schema evolution
- CI/CD pipeline for automated deployment 