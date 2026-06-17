import { CheckCircle2, Gauge, Lightbulb, ScanEye, UploadCloud } from "lucide-react";
import { useApp } from "../contexts/AppContext.jsx";

const icons = [ScanEye, Lightbulb, Gauge];

export default function QualityCard({ qualite }) {
  const { t } = useApp();
  return (
    <article className="rounded-lg border border-line bg-panel p-5 shadow-card">
      <div className="mb-4 flex items-center gap-3">
        <span className="icon-chip">
          <UploadCloud size={17} />
        </span>
        <h2 className="text-lg font-extrabold">{t("qualityTitle")}</h2>
      </div>

      <div className="flex justify-center py-1">
        <div className="quality-ring" style={{ "--score": `${qualite.score}%` }}>
          <span>{qualite.score}%</span>
        </div>
      </div>
      <p className="mb-6 text-center text-sm font-extrabold text-success">{qualite.label}</p>

      <div className="space-y-4">
        {qualite.criteres.map((item, index) => {
          const Icon = icons[index] ?? Gauge;
          return (
            <div key={item.nom} className="grid grid-cols-[22px_86px_1fr_42px] items-center gap-3">
              <Icon size={17} className="text-[#1b2b54]" />
              <span className="text-sm text-muted">{item.nom}</span>
              <span className="h-2 overflow-hidden rounded-full bg-[#dfe7f2]">
                <span className="block h-full rounded-full bg-brand" style={{ width: `${item.score}%` }} />
              </span>
              <span className="text-right text-sm font-bold text-muted">{item.score}%</span>
            </div>
          );
        })}
      </div>

      <div className="mt-7 flex items-center gap-3 rounded-lg border border-green-100 bg-green-50 px-4 py-4 text-sm font-extrabold text-[#238144]">
        <CheckCircle2 size={21} fill="currentColor" stroke="white" />
        {t("qualityEnough")}
      </div>
    </article>
  );
}
