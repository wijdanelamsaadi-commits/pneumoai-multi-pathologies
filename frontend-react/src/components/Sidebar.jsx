import { BarChart3, Clock3, FileText, Home, Info } from "lucide-react";
import { NavLink } from "react-router-dom";
import { useApp } from "../contexts/AppContext.jsx";
import LungIcon from "./LungIcon.jsx";

const nav = [
  { key: "navHome", icon: Home, to: "/" },
  { key: "navAnalysis", icon: FileText, to: "/analyse" },
  { key: "navHistory", icon: Clock3, to: "/historique" },
  { key: "navReports", icon: BarChart3, to: "/rapports" },
  { key: "navAbout", icon: Info, to: "/a-propos" }
];

export default function Sidebar() {
  const { t } = useApp();

  return (
    <aside className="border-line/80 bg-white/88 hidden min-h-screen w-[278px] border-r px-6 py-7 shadow-[12px_0_45px_rgba(19,48,103,0.05)] backdrop-blur lg:fixed lg:inset-y-0 lg:left-0 lg:block">
      <div className="flex items-center gap-3">
        <Logo />
        <div>
          <p className="text-xl font-extrabold leading-none text-[#103375]">PneumoAI</p>
          <p className="mt-2 text-sm text-muted">{t("brandSubtitle")}</p>
        </div>
      </div>

      <div className="my-7 h-px bg-line" />

      <nav className="space-y-2">
        {nav.map(({ key, icon: Icon, to }) => (
          <NavLink
            key={key}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `flex h-12 w-full items-center gap-4 rounded-lg px-4 text-left text-[15px] font-bold transition ${
                isActive
                  ? "bg-blue-50 text-brand"
                  : "text-ink hover:bg-blue-50/70 hover:text-brand"
              }`
            }
          >
            <Icon size={20} strokeWidth={2.2} />
            {t(key)}
          </NavLink>
        ))}
      </nav>

      <p className="absolute bottom-7 left-9 text-sm text-muted">{t("version")}</p>
    </aside>
  );
}

function Logo() {
  return (
    <div className="grid size-11 place-items-center rounded-2xl bg-brand text-white shadow-lg shadow-blue-200">
      <LungIcon className="size-7" strokeWidth={2.4} />
    </div>
  );
}
