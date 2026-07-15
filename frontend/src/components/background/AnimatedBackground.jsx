import { motion } from "framer-motion";

function AnimatedBackground() {
  return (
    <div className="fixed inset-0 -z-20 overflow-hidden bg-slate-950">
      <motion.div
        animate={{
          x: [0, 150, -100, 0],
          y: [0, -120, 80, 0],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute w-[500px] h-[500px] rounded-full bg-cyan-500/20 blur-3xl top-[-120px] left-[-120px]"
      />

      <motion.div
        animate={{
          x: [0, -150, 80, 0],
          y: [0, 100, -60, 0],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute w-[500px] h-[500px] rounded-full bg-violet-600/20 blur-3xl bottom-[-100px] right-[-100px]"
      />

      <motion.div
        animate={{
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
        }}
        className="absolute w-[400px] h-[400px] rounded-full bg-blue-500/10 blur-3xl left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
      />
    </div>
  );
}

export default AnimatedBackground;