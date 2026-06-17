import { Brain, ShieldCheck, UploadCloud } from "lucide-react";
import { useApp } from "../contexts/AppContext.jsx";

const steps = [
  {
    number: "1",
    title: "Upload",
    icon: UploadCloud,
    text: "Uploadez une radiographie thoracique (JPEG ou PNG).",
    color: "blue"
  },
  {
    number: "2",
    title: "Analyse",
    icon: Brain,
    text: "Le système évalue la qualité de l'image et détecte les pathologies",
    color: "blue"
  },
  {
    number: "3",
    title: "Décision",
    icon: ShieldCheck,
    text: "Diagnostic multi-pathologies avec niveau de confiance et recommandation",
    color: "green"
  }
];

export default function HowItWorks() {
  const { t } = useApp();
  return (
    <section className="mt-5 rounded-lg border border-line bg-panel p-5 shadow-card">
      <div className="mb-6 flex items-center gap-3">
        <span className="icon-chip">
          <svg viewBox="0 0 24 24" className="size-5" fill="none">
            <rect x="4" y="4" width="11" height="14" rx="1.5" stroke="currentColor" strokeWidth="2" />
            <path d="M8 8h10a2 2 0 0 1 2 2v10H8V8Z" stroke="currentColor" strokeWidth="2" />
          </svg>
        </span>
        <h2 className="text-lg font-extrabold">{t("howWorks")}</h2>
      </div>

      <div className="grid items-center gap-5 lg:grid-cols-[1fr_72px_1fr_72px_1fr]">
        {steps.map((step, index) => (
          <Step key={step.number} step={step} showArrow={index < steps.length - 1} />
        ))}
      </div>
    </section>
  );
}

function Step({ step, showArrow }) {
  const Icon = step.icon;
  return (
    <>
      <div className="flex items-center gap-5">
        <span className={`grid size-16 shrink-0 place-items-center rounded-xl border ${step.color === "green" ? "border-green-200 bg-green-50 text-success" : "border-blue-200 bg-blue-50 text-brand"}`}>
          <Icon size={36} />
        </span>
        <div>
          <div className="mb-2 flex items-center gap-3">
            <span className="grid size-7 place-items-center rounded-md bg-brand text-sm font-black text-white">
              {step.number}
            </span>
            <p className="font-extrabold">{step.title}</p>
          </div>
          <p className="text-sm leading-6 text-muted">{step.text}</p>
        </div>
      </div>
      {showArrow && (
        <div className="hidden text-center text-3xl font-black tracking-[6px] text-brand lg:block">
          ----→
        </div>
      )}
    </>
  );
}
