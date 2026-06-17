import { CheckCircle2, Clock3, FileImage, Search } from "lucide-react";
import { CardTitle, PageCard, PageIntro } from "../components/PageSection.jsx";
import { useApp } from "../contexts/AppContext.jsx";

const rows = [
  { id: "RAD-2026-001", date: "16 juin 2026", patient: "Cas anonyme A", result: "Pneumonie", score: "88%", status: "Diagnostic avec prudence" },
  { id: "RAD-2026-002", date: "15 juin 2026", patient: "Cas anonyme B", result: "Normal", score: "91%", status: "Diagnostic fiable" },
  { id: "RAD-2026-003", date: "14 juin 2026", patient: "Cas anonyme C", result: "Consolidation", score: "72%", status: "Diagnostic avec prudence" },
  { id: "RAD-2026-004", date: "13 juin 2026", patient: "Cas anonyme D", result: "Épanchement pleural", score: "64%", status: "Diagnostic avec prudence" }
];

export default function HistoryPage() {
  const { t } = useApp();
  return (
    <>
      <PageIntro
        icon={Clock3}
        title={t("historyTitle")}
        description={t("historyDesc")}
      />

      <div className="mt-7 grid gap-4 md:grid-cols-3">
        <Stat label={t("totalAnalyses")} value="128" tone="blue" mock={t("mockData")} />
        <Stat label={t("reliableDiagnoses")} value="86" tone="green" mock={t("mockData")} />
        <Stat label={t("toReview")} value="42" tone="orange" mock={t("mockData")} />
      </div>

      <PageCard className="mt-5">
        <CardTitle
          icon={FileImage}
          title={t("latestXrays")}
          action={
            <button className="flex h-10 items-center gap-2 rounded-md border border-line bg-white px-4 text-sm font-extrabold text-ink shadow-sm">
              <Search size={16} />
              {t("search")}
            </button>
          }
        />
        <div className="overflow-hidden rounded-lg border border-line">
          {rows.map((row) => (
            <div key={row.id} className="grid gap-3 border-b border-line bg-white px-4 py-4 text-sm last:border-b-0 md:grid-cols-[1.1fr_1fr_1fr_1fr_1fr] md:items-center">
              <div>
                <p className="font-extrabold text-ink">{row.id}</p>
                <p className="mt-1 text-muted">{row.date}</p>
              </div>
              <p className="font-bold text-muted">{row.patient}</p>
              <p className="font-extrabold text-ink">{row.result}</p>
              <p className="font-black text-brand">{row.score}</p>
              <span className="inline-flex w-fit items-center gap-2 rounded-full bg-orange-50 px-3 py-2 font-extrabold text-[#d75b12]">
                <CheckCircle2 size={15} />
                {row.status}
              </span>
            </div>
          ))}
        </div>
      </PageCard>
    </>
  );
}

function Stat({ label, value, tone, mock }) {
  const colors = {
    blue: "border-blue-200 bg-blue-50 text-brand",
    green: "border-green-200 bg-green-50 text-success",
    orange: "border-orange-200 bg-orange-50 text-[#d75b12]"
  };

  return (
    <PageCard>
      <p className="text-sm font-bold text-muted">{label}</p>
      <p className="mt-3 text-4xl font-black">{value}</p>
      <span className={`mt-4 inline-flex rounded-full border px-3 py-1 text-sm font-extrabold ${colors[tone]}`}>
        {mock}
      </span>
    </PageCard>
  );
}
