import {
  User,
  Stethoscope,
  Hospital,
  Pill,
} from "lucide-react";

import MedicineCard from "./MedicineCard";
import { renderValue } from "../utils/safeRender";

function PatientCard({ data }) {
  if (!data) return null;

  return (
    <div className="space-y-10">

      {/* Patient Information */}

      <div className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-2xl shadow-xl">

        <h2 className="mb-8 text-3xl font-bold text-white">
          Patient Information
        </h2>

        <div className="grid gap-6 md:grid-cols-4">

          <InfoBox
            icon={<User className="text-cyan-400" />}
            title="Patient"
            value={data.patient_name}
          />

          <InfoBox
            icon={<Stethoscope className="text-green-400" />}
            title="Doctor"
            value={data.doctor_name}
          />

          <InfoBox
            icon={<Hospital className="text-purple-400" />}
            title="Hospital"
            value={data.hospital}
          />

          <InfoBox
            icon={<Pill className="text-yellow-400" />}
            title="Medicines"
            value={`${data.medicines?.length || 0} Detected`}
          />

        </div>

      </div>

      {/* Medicines */}

      <div>

        <h2 className="mb-8 text-3xl font-bold text-white">
          Medicines Detected
        </h2>

        {data.medicines && data.medicines.length > 0 ? (

          <div className="space-y-8">

            {data.medicines.map((medicine, index) => (

              <MedicineCard
                key={index}
                medicine={medicine}
                index={index}
              />

            ))}

          </div>

        ) : (

          <div className="rounded-3xl border border-yellow-500/30 bg-yellow-500/10 p-10 text-center">

            <h3 className="text-2xl font-semibold text-yellow-300">
              No Medicines Detected
            </h3>

            <p className="mt-3 text-yellow-100">
              CuraLens AI could not identify any medicines from this prescription.
            </p>

          </div>

        )}

      </div>

    </div>
  );
}

function InfoBox({ icon, title, value }) {

  const displayValue = renderValue(value, "Not Detected");

  return (

    <div className="rounded-2xl border border-white/10 bg-white/5 p-6 transition hover:border-cyan-400/30">

      <div className="mb-4 flex items-center gap-3">

        {icon}

        <h3 className="text-lg font-semibold text-white">
          {title}
        </h3>

      </div>

      <p className="text-lg text-gray-300">

        {displayValue === "Not Detected" ? (
          <span className="text-amber-400">
            Not Detected
          </span>
        ) : (
          displayValue
        )}

      </p>

    </div>

  );

}

export default PatientCard;