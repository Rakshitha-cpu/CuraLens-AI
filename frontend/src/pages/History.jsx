import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { FileText, Calendar, Pill, ShieldAlert } from "lucide-react";

import Navbar from "../components/layout/Navbar";
import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";

function History() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const token = localStorage.getItem("token");

    if (!storedUser || !token) {
      setLoggedIn(false);
      setLoading(false);
      return;
    }

    setLoggedIn(true);

    axios
      .get("http://127.0.0.1:8000/history/me", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => setRecords(response.data))
      .catch((err) => {
        if (err.response?.status === 401) {
          // Token expired or invalid - clear it and prompt re-login
          localStorage.removeItem("token");
          localStorage.removeItem("user");
          setLoggedIn(false);
        } else {
          setError("Could not load history. Is the backend running?");
        }
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <AnimatedBackground />
      <FloatingParticles />
      <Navbar />

      <div className="relative z-10 mx-auto max-w-7xl px-8 py-20 text-white">

        <h1 className="text-5xl font-bold">
          Prescription History
        </h1>

        {!loggedIn && (
          <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-white/5 p-10 backdrop-blur-2xl">
            <p className="text-xl text-gray-300">
              Log in to see your prescription history.
            </p>
          </div>
        )}

        {loggedIn && loading && (
          <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-white/5 p-10 backdrop-blur-2xl">
            <p className="text-xl text-gray-300">Loading...</p>
          </div>
        )}

        {loggedIn && !loading && error && (
          <div className="mt-10 rounded-3xl border border-red-500/30 bg-red-500/10 p-10">
            <p className="text-xl text-red-300">{error}</p>
          </div>
        )}

        {loggedIn && !loading && !error && records.length === 0 && (
          <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-white/5 p-10 backdrop-blur-2xl">
            <p className="text-xl text-gray-300">
              No prescriptions analyzed yet. Upload one from the Home page to see it here.
            </p>
          </div>
        )}

        {loggedIn && !loading && !error && records.length > 0 && (
          <div className="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {records.map((r) => (
              <Link
                key={r.id}
                to={`/history/${r.id}`}
                className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition hover:-translate-y-1 hover:border-cyan-400/40"
              >
                <div className="flex items-center gap-3">
                  <FileText className="text-cyan-300" size={24} />
                  <h3 className="text-xl font-semibold text-white">
                    {r.patient_name || "Unknown Patient"}
                  </h3>
                </div>

                <div className="mt-4 flex items-center gap-2 text-sm text-gray-400">
                  <Calendar size={16} />
                  {r.created_at ? new Date(r.created_at).toLocaleDateString() : "Unknown date"}
                </div>

                <div className="mt-2 flex items-center gap-2 text-sm text-gray-400">
                  <Pill size={16} />
                  {r.medicine_count ?? 0} medicine(s)
                </div>

                <div className="mt-2 flex items-center gap-2 text-sm">
                  <ShieldAlert size={16} className="text-cyan-300" />
                  <span className="text-gray-300">Risk: {r.risk_level || "Unknown"}</span>
                  {r.score != null && (
                    <span className="ml-auto font-bold text-cyan-300">{r.score}%</span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}

      </div>
    </>
  );
}

export default History;