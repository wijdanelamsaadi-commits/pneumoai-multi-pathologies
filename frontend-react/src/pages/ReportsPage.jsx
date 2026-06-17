import { Download, FileText, ShieldCheck } from "lucide-react";
import { CardTitle, PageCard, PageIntro } from "../components/PageSection.jsx";
import { useApp } from "../contexts/AppContext.jsx";

const reports = [
  { title: "Rapport complet d'analyse", type: "PDF", date: "16 juin 2026", status: "Disponible" },
  { title: "Synthèse qualité image", type: "PDF", date: "16 juin 2026", status: "Disponible" },
  { title: "Export des probabilités", type: "CSV", date: "15 juin 2026", status: "Disponible" }
];

export default function ReportsPage() {
  const { t } = useApp();
  return (
    <>
      <PageIntro
        icon={FileText}
        title={t("reportsTitle")}
        description={t("reportsDesc")}
      />

      <section className="mt-7 grid gap-4 lg:grid-cols-[1fr_0.78fr]">
        <PageCard>
          <CardTitle icon={FileText} title={t("availableReports")} />
          <div className="space-y-3">
            {reports.map((report) => (
              <div key={report.title} className="flex flex-col gap-4 rounded-lg border border-line bg-white p-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="font-extrabold">{report.title}</p>
                  <p className="mt-2 text-sm text-muted">{report.type} · {report.date}</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="rounded-full bg-green-50 px-3 py-2 text-sm font-extrabold text-success">
                    {report.status}
                  </span>
                  <button className="grid size-10 place-items-center rounded-md border border-line bg-white text-ink shadow-sm">
                    <Download size={18} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </PageCard>

        <PageCard>
          <CardTitle icon={ShieldCheck} title={t("clinicalSummary")} />
          <div className="rounded-lg border border-orange-200 bg-orange-50 p-5">
            <p className="text-lg font-extrabold text-[#f15a24]">
              {t("cautiousDiagnosis")}
            </p>
            <p className="mt-3 text-sm leading-6 text-[#304062]">
              {t("clinicalText")}
            </p>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3">
            <Mini label="Qualité" value="92%" />
            <Mini label="Pneumonie" value="88%" />
            <Mini label="Consolidation" value="72%" />
            <Mini label="Normal" value="12%" />
          </div>
        </PageCard>
      </section>
    </>
  );
}

function Mini({ label, value }) {
  return (
    <div className="rounded-lg border border-line bg-white p-4">
      <p className="text-sm font-bold text-muted">{label}</p>
      <p className="mt-2 text-2xl font-black">{value}</p>
    </div>
  );
}
