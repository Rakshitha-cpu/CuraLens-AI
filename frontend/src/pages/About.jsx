import Navbar from "../components/layout/Navbar";
import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";

function About() {
  return (
    <>
      <AnimatedBackground />
      <FloatingParticles />
      <Navbar />

      <div className="relative z-10 mx-auto max-w-6xl px-8 py-20 text-white">

        <h1 className="text-5xl font-bold">
          About CuraLens AI
        </h1>

        <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-white/5 p-10 backdrop-blur-2xl">

          <p className="text-lg leading-8 text-gray-300">
            CuraLens AI is an intelligent prescription analysis platform
            that helps patients and healthcare professionals understand
            handwritten prescriptions using Artificial Intelligence.

            It extracts medicine names, verifies medicines, detects drug
            interactions, calculates prescription risk scores, and provides
            easy-to-understand medicine education.
          </p>

        </div>

      </div>
    </>
  );
}

export default About;