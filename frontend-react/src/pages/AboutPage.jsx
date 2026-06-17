import { Brain, Info, ShieldCheck } from "lucide-react";
import { CardTitle, PageCard, PageIntro } from "../components/PageSection.jsx";
import LungIcon from "../components/LungIcon.jsx";
import { useApp } from "../contexts/AppContext.jsx";

export default function AboutPage() {
  const { t } = useApp();
  return (
    <>
      <PageIntro
        icon={Info}
        title={t("aboutTitle")}
        description={t("aboutDesc")}
      />

      <section className="mt-7 grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
        <PageCard>
          <CardTitle icon={LungIcon} title="PneumoAI" />
          <p className="text-sm leading-7 text-muted">
            {t("aboutBody")}
          </p>
          <div className="mt-5 rounded-lg border border-blue-200 bg-blue-50 p-4">
            <p className="font-extrabold text-[#103375]">Version 2.0.0</p>
            <p className="mt-2 text-sm text-muted">Prototype PFE 2026 · modèle multi-label CheXpert-small</p>
          </div>
        </PageCard>

        <PageCard>
          <CardTitle icon={Brain} title={t("currentFlow")} />
          <div className="grid gap-3 md:grid-cols-3">
            <Step number="1" title="Upload" text={t("uploadTitle")} />
            <Step number="2" title={t("navAnalysis")} text="Pneumonie / Consolidation / Épanchement pleural" />
            <Step number="3" title={t("cautiousDiagnosis")} text={t("diagnosisTitle")} />
          </div>
        </PageCard>
      </section>

      <PageCard className="mt-5">
        <CardTitle icon={ShieldCheck} title={t("medicalWarning")} />
        <p className="text-sm leading-7 text-muted">
          {t("warningText")}
        </p>
      </PageCard>
    </>
  );
}

function Step({ number, title, text }) {
  return (
    <div className="rounded-lg border border-line bg-white p-4">
      <span className="grid size-7 place-items-center rounded-md bg-brand text-sm font-black text-white">
        {number}
      </span>
      <p className="mt-4 font-extrabold">{title}</p>
      <p className="mt-2 text-sm leading-6 text-muted">{text}</p>
    </div>
  );
}
