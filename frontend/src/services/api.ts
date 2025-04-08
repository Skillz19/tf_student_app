import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export interface Student {
  student_id: string;
  first_name: string;
  last_name: string;
  dob: string;
  personal_tutor_id: number;
  average_grade: number;
  classification: string;
}

export interface Module {
  id: number;
  title: string;
  module_tutor_id: number;
}

export interface Grade {
  student_id: string;
  module_id: number;
  score: number;
}

export interface Tutor {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  title?: string;
}

// Student API calls
export const getStudent = async (studentId: string): Promise<Student> => {
  const response = await axios.get(`${API_URL}/students/${studentId}/`);
  return response.data;
};

export const getAllStudents = async (): Promise<Student[]> => {
  const response = await axios.get(`${API_URL}/students/`);
  return response.data;
};

// Module API calls
export const getModule = async (moduleId: number): Promise<Module> => {
  const response = await axios.get(`${API_URL}/modules/${moduleId}/`);
  return response.data;
};

export const getAllModules = async (): Promise<Module[]> => {
  const response = await axios.get(`${API_URL}/modules/`);
  return response.data;
};

// Tutor API calls
export const getTutor = async (tutorId: number): Promise<Tutor> => {
  const response = await axios.get(`${API_URL}/tutors/${tutorId}/`);
  return response.data;
};

export const getAllTutors = async (): Promise<Tutor[]> => {
  const response = await axios.get(`${API_URL}/tutors/`);
  return response.data;
};

// Grade API calls
export const getStudentGrades = async (studentId: string): Promise<Grade[]> => {
  const response = await axios.get(`${API_URL}/students/${studentId}/grades/`);
  return response.data;
}; 