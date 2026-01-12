import { Link, useNavigate, useLocation } from "react-router-dom";

export default function Navbar() {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/catalog");
  };

  // highlight active tab
  const activeClass = (path) =>
    location.pathname.startsWith(path)
      ? "text-indigo-400 font-semibold"
      : "hover:text-indigo-400 text-gray-200";

  return (
    <nav className="bg-gray-900 border-b border-gray-800 text-white p-4 flex justify-between items-center">
      <Link to="/catalog" className="text-indigo-400 font-bold text-xl">
        🎬 LessonCMS
      </Link>

      <div className="flex gap-6 items-center">
        <Link to="/catalog" className={activeClass("/catalog")}>
          Catalog
        </Link>

        {token && (
          <Link to="/programs" className={activeClass("/programs")}>
            CMS
          </Link>
        )}

        {token ? (
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm"
          >
            Logout ({role})
          </button>
        ) : (
          <Link to="/login" className="hover:text-indigo-400 text-gray-200">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}
