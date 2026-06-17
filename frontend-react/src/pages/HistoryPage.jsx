import { Clock3, FileImage, Search } from "lucide-react";
import { CardTitle, PageCard, PageIntro } from "../components/PageSection.jsx";
import { useApp } from "../contexts/AppContext.jsx";

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
        <Stat label={t("totalAnalyses")} value="0" tone="blue" />
        <Stat label={t("reliableDiagnoses")} value="0" tone="green" />
        <Stat label={t("toReview")} value="0" tone="orange" />
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
        <div className="rounded-lg border border-blue-200 bg-blue-50/60 px-5 py-6 text-sm font-bold text-brand">
          {t("noHistory")}
        </div>
      </PageCard>
    </>
  );
}

function Stat({ label, value, tone }) {
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
        {label}
      </span>
    </PageCard>
  );
}
