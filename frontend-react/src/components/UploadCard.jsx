import { UploadCloud } from "lucide-react";
import { useApp } from "../contexts/AppContext.jsx";

export default function UploadCard({ onFileSelected }) {
  const { t } = useApp();
  const handleChange = (event) => {
    onFileSelected(event.target.files?.[0]);
  };

  return (
    <article className="rounded-lg border border-line bg-panel p-5 shadow-card">
      <div className="mb-5 flex items-center gap-3">
        <span className="grid size-7 place-items-center rounded-md bg-brand text-sm font-black text-white shadow-sm">
          1
        </span>
        <h2 className="text-lg font-extrabold">{t("uploadTitle")}</h2>
      </div>

      <label className="flex min-h-[286px] cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-blue-300 bg-white px-5 text-center transition hover:border-brand hover:bg-blue-50/40">
        <UploadCloud className="mb-4 text-brand" size={56} strokeWidth={1.8} />
        <p className="text-sm font-bold">{t("uploadDrop")}</p>
        <p className="mt-4 text-sm text-muted">{t("orText")}</p>
        <span className="mt-4 rounded-md bg-brand px-6 py-3 text-sm font-bold text-white shadow-md shadow-blue-200">
          {t("chooseFile")}
        </span>
        <p className="mt-7 text-sm text-muted">{t("acceptedFormats")}</p>
        <p className="mt-2 text-sm text-muted">{t("maxSize")}</p>
        <input className="sr-only" type="file" accept="image/png,image/jpeg" onChange={handleChange} />
      </label>
    </article>
  );
}
