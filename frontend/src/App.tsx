import { BrowserRouter as Router, Routes, Route, useParams, ScrollRestoration } from 'react-router-dom';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import StudentList from './components/StudentList';
import StudentDetail from './components/StudentDetail';
import PageTransition from './components/PageTransition';
import './index.css';

// Wrapper component to handle route parameters
const StudentDetailWrapper = () => {
  const { studentId } = useParams<{ studentId: string }>();
  
  return <StudentDetail studentId={studentId || ''} />;
};

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex flex-col">
        <Navigation />
        <main className="flex-1 py-4 container mx-auto px-4">
          <div className="min-h-[calc(100vh-theme(spacing.16))]">
            <Routes>
              <Route path="/" element={<PageTransition><Dashboard /></PageTransition>} />
              <Route path="/students" element={<PageTransition><StudentList /></PageTransition>} />
              <Route path="/students/:studentId" element={<PageTransition><StudentDetailWrapper /></PageTransition>} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
