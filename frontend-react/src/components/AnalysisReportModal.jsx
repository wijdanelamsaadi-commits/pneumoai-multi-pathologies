import { Download, Printer, X } from "lucide-react";
import { jsPDF } from "jspdf";

const orderedPathologies = [
  "Pneumonie",
  "Normal",
  "\u00c9panchement pleural",
  "Consolidation"
];

export default function AnalysisReportModal({ analysisDate, result, onClose }) {
  if (!result) return null;

  const reportRows = buildReportRows(result, analysisDate);

  const downloadPdf = () => {
    const doc = new jsPDF();
    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text("Rapport detaille d'analyse", 20, 22);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(11);
    let y = 38;
    reportRows.forEach((row) => {
      doc.setFont("helvetica", "bold");
      doc.text(`${row.label}:`, 20, y);
      doc.setFont("helvetica", "normal");
      doc.text(String(row.value), 78, y);
      y += 10;
    });

    y += 6;
    doc.setFont("helvetica", "bold");
    doc.text("Avertissement:", 20, y);
    doc.setFont("helvetica", "normal");
    doc.text("Ce resultat ne remplace pas l'avis d'un professionnel de sante.", 20, y + 9);
    doc.save("rapport-analyse-pneumoai.pdf");
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#071333]/55 px-4 py-6 backdrop-blur-sm print:static print:bg-white print:p-0">
      <section className="max-h-[92vh] w-full max-w-3xl overflow-auto rounded-2xl border border-line bg-white p-6 shadow-[0_28px_80px_rgba(7,19,51,0.28)] print:max-h-none print:border-0 print:shadow-none">
        <div className="flex items-start justify-between gap-4 border-b border-line pb-5">
          <div>
            <p className="text-sm font-extrabold uppercase tracking-wide text-brand">PneumoAI</p>
            <h2 className="mt-2 text-2xl font-black text-ink">Rapport d\u00e9taill\u00e9 d'analyse</h2>
            <p className="mt-2 text-sm text-muted">
              Synth\u00e8se g\u00e9n\u00e9r\u00e9e \u00e0 partir des r\u00e9sultats de l'analyse courante.
            </p>
          </div>
          <button
            aria-label="Fermer"
            onClick={onClose}
            className="grid size-10 shrink-0 place-items-center rounded-full border border-line bg-white text-ink shadow-sm print:hidden"
          >
            <X size={20} />
          </button>
        </div>

        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          {reportRows.map((row) => (
            <ReportField key={row.label} label={row.label} value={row.value} />
          ))}
        </div>

        <div className="mt-6 rounded-lg border border-orange-200 bg-orange-50/80 p-4">
          <p className="font-extrabold text-[#f15a24]">Avertissement</p>
          <p className="mt-2 text-sm leading-6 text-[#304062]">
            Ce r\u00e9sultat ne remplace pas l'avis d'un professionnel de sant\u00e9.
          </p>
        </div>

        <div className="mt-7 flex flex-col gap-3 border-t border-line pt-5 sm:flex-row sm:justify-end print:hidden">
          <button
            onClick={downloadPdf}
            className="flex h-11 items-center justify-center gap-2 rounded-md bg-brand px-5 text-sm font-extrabold text-white shadow-md shadow-blue-200"
          >
            <Download size={18} />
            T\u00e9l\u00e9charger PDF
          </button>
          <button
            onClick={() => window.print()}
            className="flex h-11 items-center justify-center gap-2 rounded-md border border-line bg-white px-5 text-sm font-extrabold text-ink shadow-sm"
          >
            <Printer size={18} />
            Imprimer
          </button>
          <button
            onClick={onClose}
            className="flex h-11 items-center justify-center rounded-md border border-line bg-white px-5 text-sm font-extrabold text-ink shadow-sm"
          >
            Fermer
          </button>
        </div>
      </section>
    </div>
  );
}

function ReportField({ label, value }) {
  return (
    <div className="rounded-lg border border-line bg-soft p-4">
      <p className="text-xs font-extrabold uppercase tracking-wide text-muted">{label}</p>
      <p className="mt-2 text-base font-black text-ink">{value}</p>
    </div>
  );
}

function buildReportRows(result, analysisDate) {
  const pathologies = new Map(result.pathologies.map((item) => [item.nom, item]));

  return [
    ["Date et heure de l'analyse", formatDate(analysisDate)],
    ["Nom du fichier upload\u00e9", result.fileName || "Aucun fichier charg\u00e9"],
    ["Qualit\u00e9 de l'image", formatQuality(result.qualite)],
    ...orderedPathologies.map((name) => [name, formatPathology(pathologies.get(name))]),
    ["D\u00e9cision finale", "Diagnostic avec prudence"]
  ].map(([label, value]) => ({ label, value }));
}

function formatDate(value) {
  return new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "long",
    timeStyle: "short"
  }).format(value || new Date());
}

function formatQuality(quality) {
  if (!quality) return "Non disponible";
  return `${quality.score}% - ${quality.label}`;
}

function formatPathology(pathology) {
  if (!pathology) return "Non disponible";
  return `${pathology.probabilite}% - ${pathology.description}`;
}
