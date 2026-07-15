import { useEffect, useState } from "react";
import { Brain, CheckCircle2, Loader2 } from "lucide-react";

const agents = [
  "Vision Agent",
  "OCR Agent",
  "Verification Agent",
  "Medication Education Agent",
  "Drug Interaction Agent",
  "Risk Scoring Agent",
];

function LoadingScreen() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActive((prev) => {
        if (prev < agents.length) return prev + 1;
        return prev;
      });
    }, 700);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-lg">

      <div className="w-[650px] rounded-3xl border border-cyan-500/30 bg-slate-900 p-10 shadow-2xl">

        <div className="flex items-center gap-4 mb-8">

          <Brain className="text-cyan-400" size={42} />

          <div>
            <h1 className="text-3xl font-bold text-white">
              AI Agents Working
            </h1>

            <p className="text-gray-400">
              Please wait while ScriptSense AI analyzes your prescription.
            </p>
          </div>

        </div>

        <div className="space-y-5">

          {agents.map((agent, index) => (
            <div
              key={index}
              className="flex items-center justify-between rounded-xl bg-slate-800 p-4"
            >
              <span className="text-lg text-white">{agent}</span>

              {index < active ? (
                <CheckCircle2
                  className="text-green-400"
                  size={26}
                />
              ) : (
                <Loader2
                  className="animate-spin text-cyan-400"
                  size={26}
                />
              )}
            </div>
          ))}

        </div>
      </div>

    </div>
  );
}

export default LoadingScreen;