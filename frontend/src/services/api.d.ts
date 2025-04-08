declare module 'services/api' {
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

  export function getStudent(studentId: string): Promise<Student>;
  export function getAllStudents(): Promise<Student[]>;
  export function getModule(moduleId: number): Promise<Module>;
  export function getAllModules(): Promise<Module[]>;
  export function getTutor(tutorId: number): Promise<Tutor>;
  export function getAllTutors(): Promise<Tutor[]>;
  export function getStudentGrades(studentId: string): Promise<Grade[]>;
} 