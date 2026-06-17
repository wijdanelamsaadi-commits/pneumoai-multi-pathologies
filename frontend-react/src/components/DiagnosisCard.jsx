import { CheckCircle2, Stethoscope } from "lucide-react";
import { useApp } from "../contexts/AppContext.jsx";
import LungIcon from "./LungIcon.jsx";

const config = {
  Pneumonie: {
    icon: Stethoscope,
    border: "border-red-200",
    bg: "bg-red-50",
    text: "text-danger"
  },
  Normal: {
    icon: LungIcon,
    secondaryIcon: CheckCircle2,
    border: "border-green-200",
    bg: "bg-green-50",
    text: "text-success"
  }
};

function levelFor(value, t) {
  if (value >= 80) return { label: t("probHigh"), color: "danger" };
  if (value >= 50) return { label: t("probModerate"), color: "warning" };
  return { label: t("probLow"), color: "success" };
}

export default function DiagnosisCard({ pathology }) {
  const { t } = useApp();
  const style = config[pathology.nom] ?? config.Pneumonie;
  const Icon = style.icon;
  const SecondaryIcon = style.secondaryIcon;
  const hasPrediction = pathology.probabilite > 0;
  const level = levelFor(pathology.probabilite, t);
  const status = pathology.statut;

  return (
    <article className={`rounded-lg border ${style.border} bg-white p-5 shadow-sm`}>
      <div className="flex min-h-[72px] items-start gap-4">
        <div className={`relative grid size-16 shrink-0 place-items-center rounded-full border ${style.border} ${style.bg}`}>
          <Icon className={style.text} size={36} strokeWidth={2.1} />
          {SecondaryIcon && (
            <span className="absolute -bottom-1 -right-1 grid size-6 place-items-center rounded-full border border-white bg-white shadow-sm">
              <SecondaryIcon className={style.text} size={16} strokeWidth={2.4} />
            </span>
          )}
        </div>
        <div>
          <h3 className="text-lg font-extrabold leading-7">{pathology.nom}</h3>
          <p className="text-4xl font-black leading-none">{pathology.probabilite}%</p>
        </div>
      </div>

      <div className={`mx-auto mt-5 w-[82%] rounded-full px-4 py-2 text-center text-sm font-extrabold ${hasPrediction ? `badge-${level.color}` : "border border-blue-200 bg-blue-50 text-brand"}`}>
        {hasPrediction ? level.label : "Aucune analyse effectu\u00e9e"}
      </div>

      {status && (
        <div className={`mx-auto mt-3 w-[82%] rounded-full px-4 py-2 text-center text-sm font-black ${
          status === "Positive"
            ? "border border-red-200 bg-red-50 text-danger"
            : "border border-green-200 bg-green-50 text-success"
        }`}>
          {status}
          {pathology.seuil !== null && pathology.seuil !== undefined ? ` · Seuil ${pathology.seuil}%` : ""}
        </div>
      )}

      <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className={`h-full rounded-full ${hasPrediction ? `bar-${level.color}` : "bg-brand"}`}
          style={{ width: `${pathology.probabilite}%` }}
        />
      </div>

      <p className="mt-5 min-h-[54px] text-sm leading-6 text-muted">
        {hasPrediction ? pathology.description : "Aucune analyse effectu\u00e9e"}
      </p>
    </article>
  );
}
