import { BrowserRouter as Router, Routes, Route, useParams, useNavigate } from 'react-router-dom';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import StudentList from './components/StudentList';
import StudentDetail from './components/StudentDetail';
import './index.css';

// Wrapper component to handle route parameters
const StudentDetailWrapper = () => {
  const { studentId } = useParams<{ studentId: string }>();
  const navigate = useNavigate();
  
  const handleBack = () => {
    navigate('/students');
  };
  
  return <StudentDetail studentId={studentId || ''} onBack={handleBack} />;
};

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navigation />
        <main className="py-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/students" element={<StudentList />} />
            <Route path="/students/:studentId" element={<StudentDetailWrapper />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
