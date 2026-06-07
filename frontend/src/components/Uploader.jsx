import { useCallback, useState } from "react";

function Uploader({ onFileUpload, loading }) {
  const [dragActive, setDragActive] = useState(false);

  const handleDrop = useCallback(
    async (event) => {
      event.preventDefault();
      setDragActive(false);
      const [file] = event.dataTransfer.files;
      if (file) {
        onFileUpload(file);
      }
    },
    [onFileUpload]
  );

  const handleChange = useCallback(
    async (event) => {
      const [file] = event.target.files;
      if (file) {
        onFileUpload(file);
      }
    },
    [onFileUpload]
  );

  return (
    <div className="rounded-3xl border border-slate-700 bg-slate-900/80 p-6 shadow-lg shadow-slate-900/40">
      <div
        className={`flex min-h-[220px] flex-col items-center justify-center gap-4 rounded-3xl border-2 border-dashed p-8 transition ${
          dragActive ? "border-cyan-400 bg-cyan-500/10" : "border-slate-700 bg-slate-950/60"
        }`}
        onDragOver={(event) => {
          event.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        <div className="text-center">
          <p className="text-xl font-semibold text-white">Drag & drop a JPEG image here</p>
          <p className="mt-2 text-sm text-slate-400">or click to browse</p>
        </div>
        <label className="inline-flex cursor-pointer rounded-full bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400">
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleChange}
          />
          Upload Image
        </label>
        {loading ? <p className="text-slate-300">Extracting metadata…</p> : null}
      </div>
    </div>
  );
}

export default Uploader;
