import { useState } from "react";

import Navbar from "../components/layout/Navbar";
import Hero from "../components/Hero";

import UploadCard from "../components/UploadCard";
import Dashboard from "../components/dashboard/Dashboard";

import AnimatedBackground from "../components/background/AnimatedBackground";
import FloatingParticles from "../components/background/FloatingParticles";

function Home() {
  const [result, setResult] = useState(null);
  const [preview, setPreview] = useState(null);

  return (
    <>
      <AnimatedBackground />
      <FloatingParticles />

      <Navbar />

      <Hero />

      <div className="relative z-10 min-h-screen bg-transparent px-6 pb-24 lg:px-10">

        <UploadCard
          setResult={setResult}
          setPreview={setPreview}
        />

        {result && (
          <Dashboard
            result={result}
            preview={preview}
          />
        )}

      </div>
    </>
  );
}

export default Home;