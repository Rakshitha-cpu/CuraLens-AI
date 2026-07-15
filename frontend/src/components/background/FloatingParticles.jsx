import { motion } from "framer-motion";

const particles = Array.from({ length: 35 });

function FloatingParticles() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {particles.map((_, index) => (
        <motion.div
          key={index}
          initial={{
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            opacity: 0.2,
          }}
          animate={{
            y: [null, -150],
            opacity: [0.2, 0.8, 0.2],
          }}
          transition={{
            duration: 10 + Math.random() * 10,
            repeat: Infinity,
            delay: Math.random() * 5,
          }}
          className="absolute w-2 h-2 rounded-full bg-cyan-400"
        />
      ))}
    </div>
  );
}

export default FloatingParticles;