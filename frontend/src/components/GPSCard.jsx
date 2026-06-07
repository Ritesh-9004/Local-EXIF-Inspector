function GPSCard({ data }) {
  return (
    <div className="rounded-3xl border border-slate-700 bg-slate-900/80 p-6 shadow-xl shadow-slate-950/20">
      <h2 className="text-2xl font-semibold text-white">GPS Data</h2>
      {data && Object.keys(data).length ? (
        <div className="mt-4 space-y-4">
          <div className="rounded-2xl bg-slate-950/70 p-4">
            <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">Latitude</p>
            <p className="mt-1 text-base text-slate-100">{data.latitude ?? "N/A"}</p>
          </div>
          <div className="rounded-2xl bg-slate-950/70 p-4">
            <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">Longitude</p>
            <p className="mt-1 text-base text-slate-100">{data.longitude ?? "N/A"}</p>
          </div>
          <div className="rounded-2xl bg-slate-950/70 p-4">
            <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">Altitude</p>
            <p className="mt-1 text-base text-slate-100">{data.altitude ?? "N/A"}</p>
          </div>
          <div className="rounded-2xl bg-slate-950/70 p-4">
            <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">Timestamp</p>
            <p className="mt-1 text-base text-slate-100">{data.timestamp ?? "N/A"}</p>
          </div>
        </div>
      ) : (
        <p className="mt-4 text-slate-400">No GPS coordinates were found in this image.</p>
      )}
    </div>
  );
}

export default GPSCard;
