import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Mail, Lock, Activity } from "lucide-react";

import Navbar from "../components/layout/Navbar";
import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `${API_URL}/auth/login`,
        {
          email,
          password,
        }
      );

      // Save logged-in user + real session token
      localStorage.setItem(
        "user",
        JSON.stringify(response.data.user)
      );
      localStorage.setItem("token", response.data.access_token);

      alert(response.data.message);

      // Redirect to Home page
      window.location.href = "/";
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(error.response.data.detail || "Login failed.");
      } else {
        alert("Cannot connect to backend.");
      }
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
              Welcome Back
            </h1>

            <p className="mt-3 text-gray-400">
              Login to CuraLens AI
            </p>
          </div>

          <form
            onSubmit={handleLogin}
            className="space-y-6"
          >

            <div>
              <label className="mb-2 block text-white">
                Email
              </label>

              <div className="flex items-center rounded-xl border border-white/10 bg-white/5 px-4">
                <Mail className="text-cyan-400" />

                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full bg-transparent p-4 text-white outline-none"
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
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full bg-transparent p-4 text-white outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 py-4 text-lg font-bold text-white transition hover:scale-105"
            >
              Login
            </button>

          </form>

          <p className="mt-8 text-center text-gray-400">
            Don't have an account?{" "}

            <Link
              to="/signup"
              className="font-semibold text-cyan-400 hover:underline"
            >
              Sign Up
            </Link>
          </p>

        </div>
      </div>
    </>
  );
}

export default Login;