import { Link, useLocation, useNavigate } from "react-router-dom";
import {
  Activity,
  House,
  History,
  User,
  Info,
  LogIn,
  UserPlus,
  LogOut,
} from "lucide-react";

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem("user"));

  const activeClass =
    "flex items-center gap-2 rounded-xl bg-cyan-500/20 px-4 py-2 text-cyan-300";

  const normalClass =
    "flex items-center gap-2 rounded-xl px-4 py-2 text-gray-300 transition hover:bg-white/10 hover:text-cyan-300";

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    alert("Logged out successfully.");
    navigate("/");
    window.location.reload();
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-cyan-500/20 bg-slate-950/70 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-4">

        {/* Logo */}

        <Link to="/" className="flex items-center gap-3">
          <Activity className="text-cyan-400" size={34} />

          <div>
            <h1 className="text-2xl font-bold text-white">
              CuraLens AI
            </h1>

            <p className="text-xs text-gray-400">
              AI-Powered Prescription Intelligence
            </p>
          </div>
        </Link>

        {/* Navigation */}

        <div className="flex items-center gap-3">

          <Link
            to="/"
            className={location.pathname === "/" ? activeClass : normalClass}
          >
            <House size={18} />
            Home
          </Link>

          <Link
            to="/history"
            className={location.pathname === "/history" ? activeClass : normalClass}
          >
            <History size={18} />
            History
          </Link>

          <Link
            to="/about"
            className={location.pathname === "/about" ? activeClass : normalClass}
          >
            <Info size={18} />
            About
          </Link>

          {user && (
            <Link
              to="/profile"
              className={location.pathname === "/profile" ? activeClass : normalClass}
            >
              <User size={18} />
              Profile
            </Link>
          )}

          <div className="mx-2 h-8 w-px bg-white/10"></div>

          {!user ? (
            <>
              <Link
                to="/login"
                className="flex items-center gap-2 rounded-xl border border-cyan-400/40 px-5 py-2 text-cyan-300 transition hover:bg-cyan-500/20"
              >
                <LogIn size={18} />
                Sign In
              </Link>

              <Link
                to="/signup"
                className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-5 py-2 font-semibold text-white shadow-lg transition hover:scale-105"
              >
                <UserPlus size={18} />
                Sign Up
              </Link>
            </>
          ) : (
            <>
              <span className="rounded-xl bg-cyan-500/10 px-4 py-2 text-cyan-300">
                Hi, {user.name}
              </span>

              <button
                onClick={handleLogout}
                className="flex items-center gap-2 rounded-xl bg-red-500 px-5 py-2 font-semibold text-white transition hover:bg-red-600"
              >
                <LogOut size={18} />
                Logout
              </button>
            </>
          )}

        </div>
      </div>
    </nav>
  );
}

export default Navbar;