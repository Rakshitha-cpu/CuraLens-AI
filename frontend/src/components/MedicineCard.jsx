import {
  Pill,
  CheckCircle,
  XCircle,
  AlertTriangle,
  BookOpen,
  ClipboardList,
  Utensils,
  Package,
  PhoneCall,
  BadgeInfo,
  ShieldCheck,
} from "lucide-react";
import { renderValue } from "../utils/safeRender";

function MedicineCard({ medicine, index }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl transition-all duration-300 hover:border-cyan-400/40 hover:shadow-[0_0_35px_rgba(6,182,212,.25)]">

      {/* Header */}

      <div className="mb-8 flex items-center justify-between">

        <div className="flex items-center gap-4">

          <div className="rounded-full bg-cyan-500/20 p-4">
            <Pill className="text-cyan-300" />
          </div>

          <div>

            <h2 className="text-2xl font-bold text-white">
              {renderValue(medicine.name, "Unknown Medicine")}
            </h2>

            <p className="text-gray-400">
              Medicine {index + 1}
            </p>

          </div>

        </div>

        {medicine.database_verified ? (
          <span className="rounded-full bg-green-500/20 px-4 py-2 text-green-300">
            <CheckCircle className="mr-2 inline" size={18} />
            Database Verified
          </span>
        ) : (
          <span className="rounded-full bg-yellow-500/20 px-4 py-2 text-yellow-300">
            <XCircle className="mr-2 inline" size={18} />
            AI Estimated
          </span>
        )}

      </div>

      {/* Basic Information */}

      <div className="grid gap-5 md:grid-cols-2">

        <Info title="Dosage" value={medicine.dosage} />
        <Info title="Frequency" value={medicine.frequency} />
        <Info title="Duration" value={medicine.duration} />
        <Info title="Instructions" value={medicine.instructions} />

      </div>

      {/* Database Information */}

      <div className="mt-8 grid gap-5 md:grid-cols-2">

        <Info title="Generic Name" value={medicine.generic_name} />

        <Info title="Brand Name" value={medicine.brand_name} />

        <Info title="Category" value={medicine.category} />

        <Info
          title="Prescription Required"
          value={medicine.prescription_required}
        />

      </div>

      {/* Issues */}

      {medicine.issues?.length > 0 && (

        <div className="mt-8 rounded-2xl border border-red-500/20 bg-red-500/10 p-6">

          <div className="mb-4 flex items-center gap-3">

            <AlertTriangle className="text-red-400" />

            <h3 className="text-xl font-bold text-red-300">
              Issues Found
            </h3>

          </div>

          <div className="flex flex-wrap gap-3">

            {medicine.issues.map((issue, index) => (

              <span
                key={index}
                className="rounded-full bg-red-500/20 px-4 py-2 text-red-200"
              >
                {renderValue(issue, "Issue detected")}
              </span>

            ))}

          </div>

        </div>

      )}

      {/* Medicine Education */}

      <div className="mt-10">

        <div className="mb-5 flex items-center gap-3">

          <BookOpen className="text-cyan-300" />

          <h3 className="text-2xl font-bold text-white">
            Medicine Education
          </h3>

        </div>

        <div className="grid gap-5 md:grid-cols-2">

          <Education
            icon={<ClipboardList className="text-cyan-400" />}
            title="Purpose"
            value={medicine.education?.purpose}
          />

          <Education
            icon={<Pill className="text-green-400" />}
            title="How To Take"
            value={medicine.education?.how_to_take}
          />

          <Education
            icon={<Utensils className="text-yellow-400" />}
            title="Food"
            value={medicine.education?.food_instruction}
          />

          <Education
            icon={<Package className="text-purple-400" />}
            title="Storage"
            value={medicine.education?.storage}
          />

          <Education
            icon={<ShieldCheck className="text-green-400" />}
            title="Warnings"
            value={
              Array.isArray(medicine.education?.warnings)
                ? medicine.education.warnings.join(", ")
                : medicine.education?.warnings
            }
          />

          <Education
            icon={<BadgeInfo className="text-orange-400" />}
            title="Common Side Effects"
            value={
              Array.isArray(medicine.education?.common_side_effects)
                ? medicine.education.common_side_effects.join(", ")
                : medicine.education?.common_side_effects
            }
          />

          <Education
            icon={<PhoneCall className="text-red-400" />}
            title="Call Doctor"
            value={medicine.education?.when_to_call_doctor}
          />

        </div>

      </div>

    </div>
  );
}

function Info({ title, value }) {

  const display = renderValue(value);

  return (

    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">

      <h4 className="mb-2 font-semibold text-cyan-300">
        {title}
      </h4>

      <p className="text-gray-300">

        {display !== "Not Available" ? (
          display
        ) : (
          <span className="text-amber-400">
            Not Available
          </span>
        )}

      </p>

    </div>

  );

}

function Education({ icon, title, value }) {

  const display = renderValue(value, "Information Not Available");

  return (

    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">

      <div className="mb-3 flex items-center gap-3">

        {icon}

        <h4 className="font-semibold text-white">
          {title}
        </h4>

      </div>

      <p className="text-gray-300">

        {display !== "Information Not Available" ? (
          display
        ) : (
          <span className="text-amber-400">
            Information Not Available
          </span>
        )}

      </p>

    </div>

  );

}

export default MedicineCard;