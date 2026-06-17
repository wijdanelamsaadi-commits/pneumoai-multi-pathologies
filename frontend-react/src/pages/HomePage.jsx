import {
  ArrowRight,
  Activity,
  Clock3,
  Image as ImageIcon,
  ShieldCheck,
  Stethoscope,
  Target,
} from "lucide-react";
import { Link } from "react-router-dom";
import xrayImage from "../assets/home-xray.png";
import { useApp } from "../contexts/AppContext.jsx";

export default function HomePage() {
  const { t } = useApp();

  const diseaseCards = [
    {
      icon: Stethoscope,
      title: t("pneumoniaCard"),
      text: t("pneumoniaText")
    },
    {
      icon: ShieldCheck,
      title: t("normalCard"),
      text: t("normalText")
    }
  ];

  const stats = [
    {
      icon: Target,
      value: "92%",
      label: t("statAccuracy"),
      text: t("statAccuracyText")
    },
    {
      icon: Clock3,
      value: "< 5 sec",
      label: t("statTime"),
      text: t("statTimeText")
    },
    {
      icon: ImageIcon,
      value: "1200+",
      label: t("statImages"),
      text: t("statImagesText")
    }
  ];

  return (
    <div className="pb-4">
      <section className="mt-14 grid items-center gap-12 lg:grid-cols-[0.86fr_1.14fr]">
        <div>
          <h1 className="text-5xl font-black leading-tight text-ink md:text-[58px]">
            {t("heroTitle")}
          </h1>
          <p className="mt-6 max-w-[650px] text-3xl font-black leading-tight text-brand md:text-[38px]">
            {t("heroLead")}
          </p>
          <p className="mt-6 max-w-[600px] text-lg font-medium leading-8 text-[#34436a]">
            {t("heroText")}
          </p>

          <Link
            to="/analyse"
            className="mt-9 inline-flex h-14 items-center gap-4 rounded-lg bg-brand px-7 text-base font-extrabold text-white shadow-lg shadow-blue-200 transition hover:bg-brandDark"
          >
            <Activity size={20} />
            {t("startAnalysis")}
            <ArrowRight size={20} />
          </Link>
        </div>

        <div className="flex justify-center lg:justify-end">
          <img
            src={xrayImage}
            alt="Chest X-Ray"
            className="hero-xray h-[360px] w-full max-w-[620px] rounded-2xl object-cover shadow-[0_18px_48px_rgba(34,51,92,0.18)] md:h-[420px] lg:h-[390px]"
          />
        </div>
      </section>

      <section className="mt-12 grid gap-5 lg:grid-cols-2">
        {diseaseCards.map((card) => {
          const Icon = card.icon;
          return (
            <article key={card.title} className="rounded-lg border border-line bg-white p-7 shadow-card">
              <div className="flex gap-5">
                <span className="grid size-[74px] shrink-0 place-items-center rounded-full border border-line bg-[#f1f5fb] text-[#46536f]">
                  <Icon size={36} strokeWidth={1.9} />
                </span>
                <div>
                  <h2 className="text-xl font-black leading-7">{card.title}</h2>
                  <p className="mt-4 text-base leading-7 text-[#304062]">{card.text}</p>
                </div>
              </div>
              <div className="mt-8 h-px bg-line" />
            </article>
          );
        })}
      </section>

      <section className="mt-5 grid gap-0 overflow-hidden rounded-lg border border-line bg-white shadow-card lg:grid-cols-3">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <article
              key={stat.label}
              className={`flex items-center gap-6 p-6 ${index !== stats.length - 1 ? "border-b border-line lg:border-b-0 lg:border-r" : ""}`}
            >
              <span className="grid size-[70px] shrink-0 place-items-center rounded-full border border-line bg-[#f1f5fb] text-[#46536f]">
                <Icon size={34} strokeWidth={1.9} />
              </span>
              <div>
                <p className="text-3xl font-black leading-none text-brand">{stat.value}</p>
                <p className="mt-3 font-extrabold">{stat.label}</p>
                <p className="mt-2 text-sm text-muted">{stat.text}</p>
              </div>
            </article>
          );
        })}
      </section>

      <section className="mt-6 flex items-center gap-5 rounded-lg border border-blue-200 bg-blue-50/40 px-7 py-5 shadow-sm">
        <ShieldCheck className="shrink-0 text-brand" size={36} />
        <div>
          <p className="text-lg font-black text-brand">{t("trustTitle")}</p>
          <p className="mt-2 text-sm font-medium text-muted">{t("trustText")}</p>
        </div>
      </section>
    </div>
  );
}
