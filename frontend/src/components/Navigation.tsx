import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
  const location = useLocation();
  
  const isActive = (path: string) => {
    return location.pathname === path ? 'bg-blue-700' : '';
  };
  
  return (
    <nav className="bg-blue-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-white font-bold text-xl">Student Grades</span>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  to="/"
                  className={`${isActive('/')} text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium`}
                >
                  Dashboard
                </Link>
                <Link
                  to="/students"
                  className={`${isActive('/students')} text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium`}
                >
                  Students
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      <div className="md:hidden">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <Link
            to="/"
            className={`${isActive('/')} text-white hover:bg-blue-700 block px-3 py-2 rounded-md text-base font-medium`}
          >
            Dashboard
          </Link>
          <Link
            to="/students"
            className={`${isActive('/students')} text-white hover:bg-blue-700 block px-3 py-2 rounded-md text-base font-medium`}
          >
            Students
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navigation; 