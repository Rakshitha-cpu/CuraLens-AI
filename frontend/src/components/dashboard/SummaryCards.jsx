import {
  Pill,
  ShieldCheck,
  TriangleAlert,
  Brain,
} from "lucide-react";
import { renderValue } from "../../utils/safeRender";

function SummaryCards({ result }) {
  if (!result) return null;

  const medicines = result.medicines?.length || 0;

  const verified =
    result.medicines?.filter((m) => m.verified).length || 0;

  const risk = renderValue(result.safety?.overall_risk, "UNKNOWN");

  const score = result.score?.score || 0;

  const cards = [
    {
      title: "Medicines",
      value: medicines,
      icon: Pill,
      color: "cyan",
    },
    {
      title: "Verified",
      value: verified,
      icon: ShieldCheck,
      color: "green",
    },
    {
      title: "Risk",
      value: risk,
      icon: TriangleAlert,
      color: "orange",
    },
    {
      title: "AI Score",
      value: `${score}%`,
      icon: Brain,
      color: "purple",
    },
  ];

  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">

      {cards.map((card, index) => {

        const Icon = card.icon;

        return (

          <div
            key={index}
            className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition duration-300 hover:-translate-y-2 hover:border-cyan-400/40 hover:shadow-[0_0_40px_rgba(34,211,238,.2)]"
          >

            <div className="flex items-center justify-between">

              <div>

                <p className="text-gray-400">
                  {card.title}
                </p>

                <h2 className="mt-3 text-4xl font-bold text-white">
                  {card.value}
                </h2>

              </div>

              <div className="rounded-2xl bg-cyan-500/10 p-4">

                <Icon
                  className="text-cyan-400"
                  size={34}
                />

              </div>

            </div>

          </div>

        );
      })}
    </div>
  );
}

export default SummaryCards;