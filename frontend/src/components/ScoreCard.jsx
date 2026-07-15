import {
  Brain,
  ShieldAlert,
  ShieldCheck,
  ShieldX,
  CheckCircle2,
} from "lucide-react";
import { renderValue } from "../utils/safeRender";

function ScoreCard({ score }) {
  if (!score) return null;

  const value = Number(score.score) || 0;

  let riskColor = "text-yellow-400";
  let riskBg = "bg-yellow-500/10 border-yellow-500/30";
  let RiskIcon = ShieldAlert;

  const riskLevelText = renderValue(score.risk_level, "");
  const level = String(riskLevelText).toUpperCase();

  if (level.includes("LOW")) {
    riskColor = "text-green-400";
    riskBg = "bg-green-500/10 border-green-500/30";
    RiskIcon = ShieldCheck;
  } else if (level.includes("HIGH")) {
    riskColor = "text-red-400";
    riskBg = "bg-red-500/10 border-red-500/30";
    RiskIcon = ShieldX;
  }

  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-2xl shadow-xl">

      <div className="flex items-center gap-3 mb-8">
        <Brain className="text-cyan-400" size={34} />
        <h2 className="text-3xl font-bold text-white">
          AI Prescription Score
        </h2>
      </div>

      <div className="flex justify-center mb-10">
        <div className="relative flex h-44 w-44 items-center justify-center rounded-full border-[12px] border-cyan-500 shadow-[0_0_35px_rgba(6,182,212,.4)]">

          <div className="text-center">

            <h1 className="text-5xl font-extrabold text-white">
              {value}
            </h1>

            <p className="text-cyan-300">
              /100
            </p>

          </div>

        </div>
      </div>

      <div className={`mb-8 rounded-2xl border p-5 ${riskBg}`}>
        <div className="flex items-center gap-3">

          <RiskIcon className={riskColor} size={28} />

          <div>

            <h3 className="text-white font-bold">
              Risk Level
            </h3>

            <p className={`${riskColor} font-semibold`}>
              {riskLevelText || "Unknown"}
            </p>

          </div>

        </div>
      </div>

      <div>

        <h3 className="mb-5 text-2xl font-bold text-white">
          AI Evaluation
        </h3>

        {score.reasons?.length ? (
          <div className="space-y-3">

            {score.reasons.map((reason, index) => (
              <div
                key={index}
                className="flex items-start gap-3 rounded-xl border border-white/10 bg-white/5 p-4"
              >

                <CheckCircle2
                  className="mt-1 text-cyan-400"
                  size={20}
                />

                <p className="text-gray-300">
                  {renderValue(reason, "Unspecified reason")}
                </p>

              </div>
            ))}

          </div>
        ) : (
          <div className="rounded-2xl border border-green-500/30 bg-green-500/10 p-5">

            <p className="font-semibold text-green-300">
              Excellent! No issues detected.
            </p>

          </div>
        )}

      </div>

    </div>
  );
}

export default ScoreCard;