import { useState } from "react";

function MakerNoteRow({ value }) {
  const [expanded, setExpanded] = useState(false);
  const raw = String(value);
  const preview = raw.length > 96 ? `${raw.slice(0, 96)}…` : raw;

  return (
    <div className="rounded-2xl bg-slate-950/70 p-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">MakerNote</p>
          <p className="mt-1 text-sm text-slate-400">Raw metadata block</p>
        </div>
        <button
          type="button"
          onClick={() => setExpanded((current) => !current)}
          className="rounded-full border border-slate-700 bg-slate-800/90 px-3 py-2 text-sm font-semibold text-sky-300 transition hover:border-sky-300 hover:text-white"
        >
          {expanded ? "Hide raw data" : "Show raw data"}
        </button>
      </div>

      <div className="mt-4 overflow-x-auto rounded-2xl bg-slate-900/90 p-4 font-mono text-xs leading-6 text-slate-200">
        <pre className="whitespace-pre-wrap break-words">{expanded ? raw : preview}</pre>
      </div>
    </div>
  );
}

function ExifCard({ title, data, className = "" }) {
  return (
    <div className={`rounded-3xl border border-slate-700 bg-slate-900/80 p-6 shadow-xl shadow-slate-950/20 ${className}`}>
      <h2 className="text-2xl font-semibold text-white">{title}</h2>
      {data && Object.keys(data).length ? (
        <div className="mt-4 space-y-3">
          {Object.entries(data).map(([key, value]) =>
            key === "MakerNote" ? (
              <MakerNoteRow key={key} value={value} />
            ) : (
              <div key={key} className="rounded-2xl bg-slate-950/70 p-4">
                <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">{key}</p>
                <p className="mt-1 text-base text-slate-100">{String(value)}</p>
              </div>
            )
          )}
        </div>
      ) : (
        <p className="mt-4 text-slate-400">No {title} metadata found.</p>
      )}
    </div>
  );
}

export default ExifCard;
