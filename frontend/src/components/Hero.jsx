import { motion } from "framer-motion";
import { ShieldCheck, BrainCircuit, ScanSearch } from "lucide-react";

function Hero() {
  const features = [
    {
      icon: <ScanSearch size={42} className="text-cyan-400" />,
      title: "OCR Analysis",
      desc: "Reads handwritten prescriptions with AI-powered OCR.",
    },
    {
      icon: <ShieldCheck size={42} className="text-green-400" />,
      title: "Safety Check",
      desc: "Detects interactions, allergies and missing information.",
    },
    {
      icon: <BrainCircuit size={42} className="text-purple-400" />,
      title: "AI Education",
      desc: "Explains medicines in simple language anyone can understand.",
    },
  ];

  return (
    <section className="relative overflow-hidden min-h-screen flex items-center justify-center px-6 py-24">

      <div className="max-w-7xl mx-auto text-center">

        <motion.div
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >

          <div className="inline-flex items-center rounded-full border border-cyan-400/40 bg-cyan-500/10 px-6 py-3 backdrop-blur-lg shadow-lg">
            <span className="font-semibold text-cyan-300">
              AI Powered Healthcare Assistant
            </span>
          </div>

          <h1 className="mt-8 text-6xl md:text-7xl font-extrabold text-white leading-tight">
            CuraLens AI
          </h1>

          <p className="mt-8 max-w-4xl mx-auto text-lg md:text-xl leading-9 text-gray-300">
            Upload handwritten prescriptions and let Artificial Intelligence
            extract medicines, verify prescriptions, detect drug interactions,
            calculate patient risk scores, and educate patients instantly.
          </p>

        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 80 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8"
        >

          {features.map((item, index) => (
            <motion.div
              key={index}
              whileHover={{
                y: -10,
                scale: 1.05,
              }}
              transition={{ duration: 0.3 }}
              className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl p-8 shadow-2xl"
            >

              <div className="flex justify-center">
                {item.icon}
              </div>

              <h3 className="mt-6 text-2xl font-bold text-white">
                {item.title}
              </h3>

              <p className="mt-4 text-gray-400 leading-7">
                {item.desc}
              </p>

            </motion.div>
          ))}

        </motion.div>

      </div>

    </section>
  );
}

export default Hero;