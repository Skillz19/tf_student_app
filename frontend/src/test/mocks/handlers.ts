import { http, HttpResponse } from 'msw';
import { Student, Module, Grade, Tutor } from '../../services/api';

const API_URL = 'http://127.0.0.1:8000';

// Mock data
export const mockStudents: Student[] = [
  {
    student_id: 'ST001',
    first_name: 'John',
    last_name: 'Doe',
    dob: '2000-01-01',
    personal_tutor_id: 1,
    average_grade: 0.85,
    classification: 'Distinction'
  },
  {
    student_id: 'ST002',
    first_name: 'Jane',
    last_name: 'Smith',
    dob: '2000-02-15',
    personal_tutor_id: 2,
    average_grade: 0.75,
    classification: 'Merit'
  }
];

export const mockModules: Module[] = [
  {
    id: 1,
    title: 'Mathematics',
    module_tutor_id: 1
  },
  {
    id: 2,
    title: 'Physics',
    module_tutor_id: 2
  }
];

export const mockGrades: Grade[] = [
  {
    student_id: 'ST001',
    module_id: 1,
    score: 0.88
  },
  {
    student_id: 'ST001',
    module_id: 2,
    score: 0.82
  }
];

export const mockTutors: Tutor[] = [
  {
    id: 1,
    first_name: 'Professor',
    last_name: 'Xavier',
    email: 'xavier@school.edu',
    title: 'Dr.'
  }
];

// API Handlers
export const handlers = [
  // Get all students
  http.get(`${API_URL}/students/`, () => {
    return HttpResponse.json(mockStudents);
  }),

  // Get single student
  http.get(`${API_URL}/students/:studentId`, ({ params }) => {
    const student = mockStudents.find(s => s.student_id === params.studentId);
    
    if (!student) {
      return HttpResponse.json({ message: 'Student not found' }, { status: 404 });
    }
    
    return HttpResponse.json(student);
  }),

  // Get all modules
  http.get(`${API_URL}/modules/`, () => {
    return HttpResponse.json(mockModules);
  }),

  // Get single module
  http.get(`${API_URL}/modules/:moduleId`, ({ params }) => {
    const moduleId = parseInt(params.moduleId as string);
    const module = mockModules.find(m => m.id === moduleId);
    
    if (!module) {
      return HttpResponse.json({ message: 'Module not found' }, { status: 404 });
    }
    
    return HttpResponse.json(module);
  }),

  // Get student grades
  http.get(`${API_URL}/students/:studentId/grades`, ({ params }) => {
    const grades = mockGrades.filter(g => g.student_id === params.studentId);
    return HttpResponse.json(grades);
  }),

  // Get all tutors
  http.get(`${API_URL}/tutors/`, () => {
    return HttpResponse.json(mockTutors);
  })
]; 