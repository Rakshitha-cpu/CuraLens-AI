import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { User, Mail, Lock, Activity } from "lucide-react";

import Navbar from "../components/layout/Navbar";
import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function Signup() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSignup = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/auth/register`,
        {
          name: formData.name,
          email: formData.email,
          password: formData.password,
        }
      );

      console.log(response.data);

      alert(
        "Registration Successful!\n\nA verification code has been sent to your email."
      );

      navigate("/verify-otp", {
        state: {
          email: formData.email,
        },
      });
    } catch (error) {
      console.error("Signup Error:", error);

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

          <div className="mb-10 text-center">
            <Activity
              size={60}
              className="mx-auto text-cyan-400"
            />

            <h1 className="mt-5 text-4xl font-bold text-white">
              Create Account
            </h1>

            <p className="mt-3 text-gray-400">
              Join CuraLens AI
            </p>
          </div>

          <form
            onSubmit={handleSignup}
            className="space-y-6"
          >

            <div>
              <label className="mb-2 block text-white">
                Full Name
              </label>

              <div className="flex items-center rounded-xl border border-white/10 bg-white/5 px-4">
                <User className="text-cyan-400" />

                <input
                  type="text"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Enter your full name"
                  className="w-full bg-transparent p-4 text-white placeholder-gray-400 outline-none"
                />
              </div>
            </div>

            <div>
              <label className="mb-2 block text-white">
                Email
              </label>

              <div className="flex items-center rounded-xl border border-white/10 bg-white/5 px-4">
                <Mail className="text-cyan-400" />

                <input
                  type="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter your email"
                  className="w-full bg-transparent p-4 text-white placeholder-gray-400 outline-none"
                />
              </div>
            </div>

            <div>
              <label className="mb-2 block text-white">
                Password
              </label>

              <div className="flex items-center rounded-xl border border-white/10 bg-white/5 px-4">
                <Lock className="text-cyan-400" />

                <input
                  type="password"
                  name="password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Create password"
                  className="w-full bg-transparent p-4 text-white placeholder-gray-400 outline-none"
                />
              </div>
            </div>

            <div>
              <label className="mb-2 block text-white">
                Confirm Password
              </label>

              <div className="flex items-center rounded-xl border border-white/10 bg-white/5 px-4">
                <Lock className="text-cyan-400" />

                <input
                  type="password"
                  name="confirmPassword"
                  required
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Confirm password"
                  className="w-full bg-transparent p-4 text-white placeholder-gray-400 outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 py-4 text-lg font-bold text-white transition duration-300 hover:scale-105 hover:shadow-lg hover:shadow-cyan-500/40 disabled:opacity-50"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>

          </form>

          <p className="mt-8 text-center text-gray-400">
            Already have an account?{" "}

            <Link
              to="/login"
              className="font-semibold text-cyan-400 hover:underline"
            >
              Login
            </Link>
          </p>

        </div>
      </div>
    </>
  );
}

export default Signup;