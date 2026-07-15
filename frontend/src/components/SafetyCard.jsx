import {
  ShieldAlert,
  AlertTriangle,
} from "lucide-react";
import { renderValue } from "../utils/safeRender";

function SafetyCard({ safety }) {
  if (!safety) return null;

  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-8">

      <div className="flex items-center gap-3 mb-6">

        <ShieldAlert
          className="text-red-400"
          size={32}
        />

        <h2 className="text-3xl font-bold text-white">
          Safety Analysis
        </h2>

      </div>

      <div className="mb-6">

        <p className="text-gray-400">
          Overall Risk
        </p>

        <h3 className="text-2xl font-bold text-red-400">
          {renderValue(safety.overall_risk, "Unknown")}
        </h3>

      </div>

      <div className="space-y-4">

        {safety.alerts?.length > 0 ? (

          safety.alerts.map((alert, index) => (

            <div
              key={index}
              className="rounded-xl border border-red-500/20 bg-red-500/10 p-4"
            >

              <div className="flex items-center gap-2">

                <AlertTriangle
                  className="text-red-400"
                  size={18}
                />

                <span className="font-semibold text-red-300">
                  {renderValue(alert.type, "Alert")}
                </span>

              </div>

              <p className="mt-2 text-gray-300">
                <strong>Medicine:</strong> {renderValue(alert.medicine)}
              </p>

              <p className="text-gray-300">
                {renderValue(alert.message, "No details provided.")}
              </p>

              <p className="text-yellow-300">
                Severity: {renderValue(alert.severity, "Unknown")}
              </p>

            </div>

          ))

        ) : (

          <div className="rounded-xl border border-green-500/30 bg-green-500/10 p-5">

            <p className="text-green-300">
              No safety issues detected.
            </p>

          </div>

        )}

      </div>

    </div>
  );
}

export default SafetyCard;