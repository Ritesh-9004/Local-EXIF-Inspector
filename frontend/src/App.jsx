import { useState } from "react";
import Uploader from "./components/Uploader";
import ExifCard from "./components/ExifCard";
import GPSCard from "./components/GPSCard";

// Use a relative URL by default so Vite dev server proxy handles requests during development.
// To override in production, set VITE_API_URL in your environment.
const API_URL = import.meta.env.VITE_API_URL || "";

function App() {
  const [metadata, setMetadata] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleFileUpload(file) {
    setSuccess("");
    setLoading(true);
    setError("");
    setMetadata(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/extract`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Unable to extract EXIF data");
      }

      const json = await response.json();
      setMetadata(json.metadata);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    const confirmed = window.confirm(
      "Clear the uploaded image and extracted metadata? This will remove the current data from the app."
    );
    if (!confirmed) {
      return;
    }

    setMetadata(null);
    setError("");
    setSuccess("Image and metadata cleared from the current session.");
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl p-6">
        <header className="mb-8 rounded-3xl border border-slate-700 bg-slate-900/80 p-8 shadow-xl shadow-slate-900/50">
          <h1 className="text-4xl font-semibold text-white">EXIF Extractor</h1>
          <p className="mt-2 max-w-2xl text-slate-400">
            Upload an image and view extracted EXIF metadata from JPEG, PNG, and TIFF files. Other image formats are detected and rejected with a clear error.
          </p>
        </header>

        <Uploader onFileUpload={handleFileUpload} loading={loading} />

        {success ? (
          <div className="mt-6 rounded-2xl bg-emerald-500/15 p-4 text-emerald-100 ring-1 ring-emerald-500/40">
            {success}
          </div>
        ) : null}

        {error ? (
          <div className="mt-6 rounded-2xl bg-rose-500/20 p-4 text-rose-100 ring-1 ring-rose-500/40">
            <strong>Error:</strong> {error}
          </div>
        ) : null}

        {metadata ? (
          <>
            <div className="mt-8 grid gap-6 lg:grid-cols-2">
              {metadata.png ? (
                <ExifCard title="PNG Metadata" data={metadata.png} />
              ) : (
                <>
                  <div>
                    <ExifCard title="IFD0" data={metadata.ifd0} />
                    <ExifCard title="EXIF" data={metadata.exif} className="mt-6" />
                  </div>
                  <GPSCard data={metadata.gps} />
                </>
              )}
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={handleClear}
                className="rounded-full border border-slate-700 bg-rose-500/10 px-5 py-3 text-sm font-semibold text-rose-200 transition hover:border-rose-400 hover:bg-rose-500/20 hover:text-white"
              >
                Clear image & metadata
              </button>
            </div>
          </>
        ) : (
          <div className="mt-8 rounded-3xl border border-dashed border-slate-700 bg-slate-900/70 p-8 text-slate-400">
            <p>No metadata extracted yet. Upload a JPEG, PNG, or TIFF image to begin.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
