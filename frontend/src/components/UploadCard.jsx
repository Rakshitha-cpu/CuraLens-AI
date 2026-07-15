import { useState } from "react";
import axios from "axios";
import {
  Upload,
  FileImage,
  Sparkles,
  CheckCircle2,
  Loader2,
} from "lucide-react";

import LoadingScreen from "./LoadingScreen";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function UploadCard({ setResult, setPreview }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];

    if (!selected) return;

    setFile(selected);

    if (selected.type.startsWith("image/")) {
      setPreview(URL.createObjectURL(selected));
    } else {
      setPreview(null);
    }

    // Reset the input value so selecting the SAME file again
    // (e.g. retrying after a failed analysis) still fires onChange.
    // Without this, the browser sees an unchanged value and the
    // handler never re-runs, leaving React stuck on stale file state.
    e.target.value = "";
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a prescription.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // If logged in, attach the real signed token so the backend can
    // verify identity and save this analysis to History. Previously
    // this sent a raw user_id, which anyone could edit in devtools -
    // a Bearer token is verified server-side and can't be spoofed.
    const token = localStorage.getItem("token");
    const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};

    try {
      setLoading(true);

      const response = await axios.post(
        `${API_URL}/ai/test`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            ...authHeaders,
          },
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(error.response.data.detail || "Analysis Failed");
      } else {
        alert("Cannot connect to backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {loading && <LoadingScreen />}

      <div className="mx-auto mt-12 max-w-4xl rounded-[32px] border border-cyan-500/20 bg-white/5 p-10 backdrop-blur-3xl shadow-[0_0_60px_rgba(6,182,212,.15)]">

        <div className="flex flex-col items-center">

          <div className="rounded-full bg-cyan-500/20 p-6 shadow-lg shadow-cyan-500/30">
            <Upload size={48} className="text-cyan-300" />
          </div>

          <h2 className="mt-6 text-4xl font-bold text-white">
            Upload Prescription
          </h2>

          <p className="mt-3 max-w-2xl text-center text-gray-300">
            Upload a handwritten or printed prescription and let
            <span className="font-semibold text-cyan-300">
              {" "}CuraLens AI{" "}
            </span>
            analyze medicines, detect interactions and educate patients.
          </p>

          <label className="mt-10 flex w-full cursor-pointer flex-col items-center rounded-3xl border border-cyan-400/30 bg-cyan-500/5 p-12 transition-all duration-300 hover:scale-[1.02] hover:border-cyan-400 hover:bg-cyan-500/10">

            <FileImage
              size={70}
              className="text-cyan-300"
            />

            <h3 className="mt-6 text-2xl font-semibold text-white">
              Click to Choose Prescription
            </h3>

            <p className="mt-2 text-gray-400">
              Supported Formats
            </p>

            <p className="font-semibold text-cyan-300">
              JPG • PNG • PDF
            </p>

            {file ? (
              <div className="mt-8 w-full rounded-2xl border border-green-500/30 bg-green-500/10 p-5">

                <div className="flex items-center gap-3">

                  <CheckCircle2
                    className="text-green-400"
                    size={30}
                  />

                  <div>
                    <p className="font-semibold text-green-300">
                      {file.name}
                    </p>

                    <p className="text-sm text-green-200">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>

                </div>

              </div>
            ) : (
              <div className="mt-8 rounded-xl border border-white/10 bg-white/5 px-6 py-4">
                <p className="text-gray-400">
                  No file selected
                </p>
              </div>
            )}

            <input
              hidden
              type="file"
              accept="image/*,.pdf"
              onChange={handleFileChange}
            />

          </label>

          <button
            onClick={handleUpload}
            disabled={loading}
            className="mt-10 flex items-center gap-3 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 px-10 py-5 text-lg font-bold text-white shadow-lg shadow-cyan-500/40 transition-all duration-300 hover:scale-105 hover:shadow-cyan-400/60 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2
                  className="animate-spin"
                  size={22}
                />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles size={22} />
                Analyze with AI
              </>
            )}
          </button>

        </div>

      </div>
    </>
  );
}

export default UploadCard;