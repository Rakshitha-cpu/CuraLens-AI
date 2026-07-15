import { Navigate } from "react-router-dom";
import Navbar from "../components/layout/Navbar";
import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";
import { UserCircle, Mail } from "lucide-react";

function Profile() {
  // Get logged-in user
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem("user"));
  } catch {
    user = null;
  }

  // If not logged in, redirect to Login page
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <>
      <AnimatedBackground />
      <FloatingParticles />
      <Navbar />

      <div className="relative z-10 mx-auto max-w-4xl px-8 py-20">

        <div className="rounded-3xl border border-cyan-500/20 bg-white/5 p-10 backdrop-blur-2xl shadow-2xl">

          <div className="flex flex-col items-center">

            <UserCircle
              size={110}
              className="text-cyan-400"
            />

            <h1 className="mt-6 text-4xl font-bold text-white">
              {user.name}
            </h1>

            <div className="mt-4 flex items-center gap-2 text-cyan-300">
              <Mail size={18} />
              <span>{user.email}</span>
            </div>

            <div className="mt-10 w-full rounded-2xl border border-cyan-500/20 bg-slate-900/40 p-6">

              <h2 className="mb-6 text-2xl font-semibold text-white">
                Account Information
              </h2>

              <div className="space-y-5">

                <div>
                  <p className="text-sm text-gray-400">
                    Full Name
                  </p>

                  <p className="text-lg text-white">
                    {user.name}
                  </p>
                </div>

                <div>
                  <p className="text-sm text-gray-400">
                    Email Address
                  </p>

                  <p className="text-lg text-white">
                    {user.email}
                  </p>
                </div>

                <div>
                  <p className="text-sm text-gray-400">
                    Account Status
                  </p>

                  <span className="inline-block rounded-full bg-green-500/20 px-4 py-2 text-green-400">
                    Verified User
                  </span>
                </div>

              </div>

            </div>

          </div>

        </div>

      </div>
    </>
  );
}

export default Profile;