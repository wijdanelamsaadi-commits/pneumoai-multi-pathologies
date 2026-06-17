import { CheckCircle2, UploadCloud } from "lucide-react";
import placeholderImage from "../assets/analysis-placeholder.png";
import { useApp } from "../contexts/AppContext.jsx";

export default function PreviewCard({ previewUrl }) {
  const { t } = useApp();
  return (
    <article className="rounded-lg border border-line bg-panel p-5 shadow-card">
      <div className="mb-5 flex items-center gap-3">
        <span className="icon-chip">
          <UploadCloud size={17} />
        </span>
        <h2 className="text-lg font-extrabold">{t("previewTitle")}</h2>
      </div>

      <div className="h-[250px] overflow-hidden rounded-md bg-black">
        {previewUrl ? (
          <img className="h-full w-full object-cover grayscale" src={previewUrl} alt="Aperçu de la radiographie" />
        ) : (
          <img
            className="h-full w-full object-cover"
            src={placeholderImage}
            alt="Image par défaut avant analyse"
          />
        )}
      </div>

      {previewUrl && (
        <p className="mt-5 flex items-center gap-3 text-sm font-medium text-muted">
          <CheckCircle2 className="text-success" size={20} fill="currentColor" stroke="white" />
          {t("imageLoaded")}
        </p>
      )}
    </article>
  );
}
