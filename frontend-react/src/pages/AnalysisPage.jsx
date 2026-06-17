import { useEffect, useState } from "react";
import { Info } from "lucide-react";
import AnalysisReportModal from "../components/AnalysisReportModal.jsx";
import DecisionBanner from "../components/DecisionBanner.jsx";
import DiagnosisCard from "../components/DiagnosisCard.jsx";
import HowItWorks from "../components/HowItWorks.jsx";
import PreviewCard from "../components/PreviewCard.jsx";
import QualityCard from "../components/QualityCard.jsx";
import UploadCard from "../components/UploadCard.jsx";
import { useApp } from "../contexts/AppContext.jsx";
import { analyzeImage, emptyAnalysisResult } from "../services/api.js";

const defaultResult = emptyAnalysisResult;

export default function AnalysisPage() {
  const { t } = useApp();
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(defaultResult);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [apiError, setApiError] = useState("");
  const [analysisDate, setAnalysisDate] = useState(new Date());
  const [isReportOpen, setIsReportOpen] = useState(false);
  const [hasAnalysis, setHasAnalysis] = useState(false);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileSelected = async (file) => {
    if (!file) return;
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(URL.createObjectURL(file));
    setIsAnalyzing(true);
    setApiError("");
    setAnalysisDate(new Date());

    try {
      setResult(await analyzeImage(file));
      setHasAnalysis(true);
    } catch (error) {
      setApiError(error.message || t("apiError"));
      setResult({
        ...emptyAnalysisResult,
        fileName: file.name
      });
      setHasAnalysis(false);
      console.error(error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <>
      <section className="mt-7 flex items-center gap-3 rounded-lg border border-blue-200 bg-blue-50/60 px-5 py-4 text-[15px] font-semibold text-brand shadow-sm">
        <span className="grid size-6 shrink-0 place-items-center rounded-full border border-brand text-brand">
          <Info size={15} />
        </span>
        <p>
          {t("analysisInfo")}
        </p>
      </section>

      {(isAnalyzing || apiError) && (
        <section
          className={`mt-4 rounded-lg border px-5 py-4 text-sm font-bold shadow-sm ${
            apiError
              ? "border-orange-200 bg-orange-50 text-[#d75b12]"
              : "border-blue-200 bg-blue-50 text-brand"
          }`}
        >
          {apiError || t("apiLoading")}
        </section>
      )}

      <section className="mt-7 grid gap-4 xl:grid-cols-[1.12fr_0.9fr_1.08fr]">
        <UploadCard onFileSelected={handleFileSelected} />
        <PreviewCard previewUrl={previewUrl} />
        <QualityCard qualite={result.qualite} />
      </section>

      <section className="mt-5 rounded-lg border border-line bg-panel p-5 shadow-card">
        <div className="mb-5 flex items-center gap-3">
          <span className="icon-chip">
            <svg viewBox="0 0 24 24" className="size-5" fill="none">
              <path
                d="M7 4v7a5 5 0 0 0 10 0V4M7 11H5a3 3 0 0 1-3-3V6m15 5h2a3 3 0 0 0 3-3V6"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          </span>
          <h2 className="text-lg font-extrabold">
            {t("diagnosisTitle")}
          </h2>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {result.pathologies.map((item) => (
            <DiagnosisCard key={item.nom} pathology={item} />
          ))}
        </div>
        {hasAnalysis ? (
          <DecisionBanner onOpenReport={() => setIsReportOpen(true)} />
        ) : (
          <div className="mt-6 rounded-lg border border-blue-200 bg-blue-50/60 px-5 py-4 text-sm font-extrabold text-brand">
            Aucune analyse effectuée
          </div>
        )}
      </section>

      <HowItWorks />

      {isReportOpen && hasAnalysis && (
        <AnalysisReportModal
          analysisDate={analysisDate}
          result={result}
          onClose={() => setIsReportOpen(false)}
        />
      )}
    </>
  );
}
