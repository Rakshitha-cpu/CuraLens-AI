import { ImageIcon } from "lucide-react";

function PrescriptionViewer({ preview }) {
  return (
    <div className="rounded-3xl border border-cyan-500/20 bg-white/5 p-6 backdrop-blur-2xl shadow-xl">

      <h2 className="mb-6 text-3xl font-bold text-white">
        Uploaded Prescription
      </h2>

      {preview ? (
        <div className="overflow-hidden rounded-2xl border border-white/10">

          <img
            src={preview}
            alt="Prescription"
            className="w-full rounded-2xl object-contain transition duration-500 hover:scale-105"
          />

        </div>
      ) : (
        <div className="flex h-[500px] flex-col items-center justify-center rounded-2xl border-2 border-dashed border-cyan-500/20 bg-slate-900/30">

          <ImageIcon
            size={80}
            className="text-cyan-400"
          />

          <p className="mt-6 text-xl font-semibold text-white">
            No Preview Available
          </p>

          <p className="mt-2 text-gray-400">
            Upload an image prescription to preview it here.
          </p>

        </div>
      )}

    </div>
  );
}

export default PrescriptionViewer;