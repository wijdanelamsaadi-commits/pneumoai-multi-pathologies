import { AlertTriangle, FileText } from "lucide-react";
import { useApp } from "../contexts/AppContext.jsx";

export default function DecisionBanner({ onOpenReport }) {
  const { t } = useApp();
  return (
    <div className="mt-6 flex flex-col gap-4 rounded-lg border border-orange-200 bg-orange-50/80 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-4">
        <span className="grid size-10 shrink-0 place-items-center rounded-lg bg-white text-[#fb6d18]">
          <AlertTriangle size={22} />
        </span>
        <div>
          <p className="text-lg font-extrabold text-[#f15a24]">{t("decisionLabel")}</p>
          <p className="mt-1 text-sm font-medium text-[#304062]">
            {t("decisionText")}
          </p>
        </div>
      </div>
      <button
        onClick={onOpenReport}
        className="flex h-11 items-center justify-center gap-2 rounded-md border border-line bg-white px-4 text-sm font-extrabold shadow-sm"
      >
        <FileText size={18} />
        {t("reportButton")}
      </button>
    </div>
  );
}
