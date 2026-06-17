export function PageIntro({ icon: Icon, title, description }) {
  return (
    <section className="mt-7 flex items-center gap-3 rounded-lg border border-blue-200 bg-blue-50/60 px-5 py-4 text-[15px] font-semibold text-brand shadow-sm">
      <span className="grid size-8 shrink-0 place-items-center rounded-lg bg-white text-brand shadow-sm">
        <Icon size={18} />
      </span>
      <div>
        <h2 className="text-lg font-extrabold text-[#103375]">{title}</h2>
        <p className="mt-1 text-sm font-semibold text-brand">{description}</p>
      </div>
    </section>
  );
}

export function PageCard({ children, className = "" }) {
  return (
    <section className={`rounded-lg border border-line bg-panel p-5 shadow-card ${className}`}>
      {children}
    </section>
  );
}

export function CardTitle({ icon: Icon, title, action }) {
  return (
    <div className="mb-5 flex items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <span className="icon-chip">
          <Icon size={17} />
        </span>
        <h2 className="text-lg font-extrabold">{title}</h2>
      </div>
      {action}
    </div>
  );
}
