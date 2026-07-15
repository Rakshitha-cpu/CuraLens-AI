import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

import Navbar from "../components/layout/Navbar";
import Dashboard from "../components/dashboard/Dashboard";
import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";

function HistoryDetail() {
  const { id } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    axios
      .get(`http://127.0.0.1:8000/history/detail/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      })
      .then((response) => setResult(response.data))
      .catch(() => setError("Could not load this prescription."))
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <>
      <AnimatedBackground />
      <FloatingParticles />
      <Navbar />

      <div className="relative z-10 min-h-screen bg-transparent px-6 pb-24 pt-32 lg:px-10">

        {loading && (
          <p className="text-center text-xl text-gray-300">Loading...</p>
        )}

        {!loading && error && (
          <p className="text-center text-xl text-red-300">{error}</p>
        )}

        {!loading && !error && result && (
          // No image preview available for a re-opened past record -
          // only the original upload session has that in memory.
          <Dashboard result={result} preview={null} />
        )}

      </div>
    </>
  );
}

export default HistoryDetail;
