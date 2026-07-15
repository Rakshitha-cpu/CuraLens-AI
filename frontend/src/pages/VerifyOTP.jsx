import { useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { MailCheck, ShieldCheck } from "lucide-react";

import Navbar from "../components/layout/Navbar";
import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function VerifyOTP() {
  const location = useLocation();
  const navigate = useNavigate();

  const email = location.state?.email || "";

  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);

  const handleVerify = async (e) => {
    e.preventDefault();

    if (!otp) {
      alert("Please enter the OTP.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/auth/verify-otp`,
        {
          email,
          otp,
        }
      );

      alert(response.data.message);

      navigate("/login");
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(error.response.data.detail);
      } else {
        alert("Unable to connect to backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <AnimatedBackground />
      <FloatingParticles />
      <Navbar />

      <div className="relative z-10 flex min-h-[85vh] items-center justify-center px-6">

        <div className="w-full max-w-md rounded-3xl border border-cyan-500/20 bg-white/5 p-10 backdrop-blur-2xl shadow-2xl">

          <div className="text-center">

            <ShieldCheck
              size={60}
              className="mx-auto text-cyan-400"
            />

            <h1 className="mt-5 text-4xl font-bold text-white">
              Verify Email
            </h1>

            <p className="mt-3 text-gray-400">
              Enter the verification code sent to
            </p>

            <p className="mt-1 break-all font-semibold text-cyan-400">
              {email}
            </p>

          </div>

          <form
            onSubmit={handleVerify}
            className="mt-10 space-y-6"
          >

            <div>

              <label className="mb-2 block text-white">
                Verification Code
              </label>

              <div className="flex items-center rounded-xl border border-white/10 bg-white/5 px-4">

                <MailCheck className="text-cyan-400" />

                <input
                  type="text"
                  required
                  maxLength={6}
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  placeholder="Enter 6-digit OTP"
                  className="w-full bg-transparent p-4 text-white placeholder-gray-400 outline-none"
                />

              </div>

            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 py-4 text-lg font-bold text-white transition hover:scale-105 disabled:opacity-50"
            >
              {loading ? "Verifying..." : "Verify Email"}
            </button>

          </form>

          <p className="mt-8 text-center text-gray-400">

            Already verified?

            <Link
              to="/login"
              className="ml-2 font-semibold text-cyan-400 hover:underline"
            >
              Login
            </Link>

          </p>

        </div>

      </div>
    </>
  );
}

export default VerifyOTP;