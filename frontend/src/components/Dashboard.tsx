import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Student, getAllStudents } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        setLoading(true);
        const data = await getAllStudents();
        setStudents(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch students data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  const calculateStats = () => {
    if (students.length === 0) return null;

    const totalStudents = students.length;
    const distinctionCount = students.filter(s => s.classification === 'Distinction').length;
    const meritCount = students.filter(s => s.classification === 'Merit').length;
    const passCount = students.filter(s => s.classification === 'Pass').length;
    const failCount = students.filter(s => s.classification === 'Fail').length;

    const totalAverage = students.reduce((sum, student) => sum + student.average_grade, 0) / totalStudents;
    const highestAverage = Math.max(...students.map(s => s.average_grade));
    const lowestAverage = Math.min(...students.map(s => s.average_grade));

    return {
      totalStudents,
      distinctionCount,
      meritCount,
      passCount,
      failCount,
      totalAverage,
      highestAverage,
      lowestAverage
    };
  };

  const formatGrade = (grade: number) => {
    return `${(grade * 100).toFixed(1)}%`;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div 
          className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"
          role="status"
          aria-label="Loading"
        >
          <span className="sr-only">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error!</strong>
        <span className="block sm:inline"> {error}</span>
      </div>
    );
  }

  const stats = calculateStats();
  if (!stats) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No student data available.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Student Performance Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">
              Total Students
            </dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">
              {stats.totalStudents}
            </dd>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">
              Average Grade
            </dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">
              {formatGrade(stats.totalAverage)}
            </dd>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">
              Highest Grade
            </dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">
              {formatGrade(stats.highestAverage)}
            </dd>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">
              Lowest Grade
            </dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">
              {formatGrade(stats.lowestAverage)}
            </dd>
          </div>
        </div>
      </div>
      
      <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-8">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Classification Breakdown
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Distribution of students by classification.
          </p>
        </div>
        <div className="border-t border-gray-200">
          <dl>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Distinction</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                  {stats.distinctionCount} ({((stats.distinctionCount / stats.totalStudents) * 100).toFixed(1)}%)
                </span>
              </dd>
            </div>
            <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Merit</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                  {stats.meritCount} ({((stats.meritCount / stats.totalStudents) * 100).toFixed(1)}%)
                </span>
              </dd>
            </div>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Pass</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                  {stats.passCount} ({((stats.passCount / stats.totalStudents) * 100).toFixed(1)}%)
                </span>
              </dd>
            </div>
            <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Fail</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                  {stats.failCount} ({((stats.failCount / stats.totalStudents) * 100).toFixed(1)}%)
                </span>
              </dd>
            </div>
          </dl>
        </div>
      </div>
      
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Grade Distribution
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Visual representation of student grades.
          </p>
        </div>
        <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
          <div className="flex">
            {/* Vertical axis */}
            <div className="flex flex-col justify-between pr-2 text-xs text-gray-500 w-12">
              <span>100%</span>
              <span>75%</span>
              <span>50%</span>
              <span>25%</span>
              <span>0%</span>
            </div>
            {/* Grid lines and bars */}
            <div className="flex-1">
              {/* Grid lines */}
              <div className="relative h-64">
                <div className="absolute w-full border-t border-gray-200" style={{ bottom: '100%' }}></div>
                <div className="absolute w-full border-t border-gray-200" style={{ bottom: '75%' }}></div>
                <div className="absolute w-full border-t border-gray-200" style={{ bottom: '50%' }}></div>
                <div className="absolute w-full border-t border-gray-200" style={{ bottom: '25%' }}></div>
                <div className="absolute w-full border-t border-gray-200" style={{ bottom: '0%' }}></div>
                {/* Bars */}
                <div className="relative h-full flex items-end space-x-1">
                  {students.map((student) => (
                    <div 
                      key={student.student_id} 
                      className="flex-1 bg-blue-500 hover:bg-blue-600 transition-colors cursor-pointer"
                      style={{ 
                        height: `${student.average_grade * 100}%`,
                        minHeight: '2px'
                      }}
                      onClick={() => navigate(`/students/${student.student_id}`)}
                      title={`${student.first_name} ${student.last_name}: ${formatGrade(student.average_grade)}`}
                      role="button"
                      aria-label={`View details for ${student.first_name} ${student.last_name}`}
                    ></div>
                  ))}
                </div>
              </div>
            </div>
          </div>
          <div className="mt-2 text-xs text-gray-500 text-center">
            Student Grades
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 