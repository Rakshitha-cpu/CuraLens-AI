import { useState } from "react";
import axios from "axios";
import { FileDown, Loader2 } from "lucide-react";

function DownloadReportButton({ result }) {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    if (!result) {
      alert("No analysis data to generate a report from.");
      return;
    }

    try {
      setDownloading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/ai/report",
        result,
        {
          responseType: "blob", // important: tells axios to expect binary data
        }
      );

      // Create a temporary URL for the PDF blob and trigger download
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "CuraLens_AI_Report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Failed to generate report. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <button
      onClick={handleDownload}
      disabled={downloading}
      className="mt-6 flex items-center gap-3 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 px-8 py-4 text-lg font-bold text-white shadow-lg shadow-emerald-500/40 transition-all duration-300 hover:scale-105 hover:shadow-emerald-400/60 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {downloading ? (
        <>
          <Loader2 className="animate-spin" size={22} />
          Generating Report...
        </>
      ) : (
        <>
          <FileDown size={22} />
          Download AI Report
        </>
      )}
    </button>
  );
}

export default DownloadReportButton;