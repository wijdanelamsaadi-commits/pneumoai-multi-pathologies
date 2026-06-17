import { ChevronDown, Globe2, Moon, Sun, UserCircle } from "lucide-react";
import { useLocation } from "react-router-dom";
import { useApp } from "../contexts/AppContext.jsx";
import LungIcon from "./LungIcon.jsx";

export default function Header() {
  const { pathname } = useLocation();
  const isHome = pathname === "/";
  const { language, languages, setLanguage, theme, toggleTheme, t } = useApp();

  return (
    <header className={`flex ${isHome ? "justify-end" : "flex-col gap-5 md:flex-row md:items-start md:justify-between"}`}>
      {!isHome && (
        <div className="flex items-center gap-5">
          <div className="grid size-16 place-items-center rounded-[22px] bg-brand text-white shadow-xl shadow-blue-200">
            <LungIcon className="size-11" strokeWidth={2.6} />
          </div>
          <div>
            <h1 className="text-3xl font-black leading-tight tracking-normal text-ink sm:text-4xl">
              {t("headerTitle")}
            </h1>
            <p className="mt-3 text-base font-medium text-muted">{t("headerSubtitle")}</p>
          </div>
        </div>
      )}

      <div className="flex shrink-0 items-center gap-3">
        <IconButton onClick={toggleTheme} label={theme === "dark" ? t("lightMode") : t("darkMode")}>
          {theme === "dark" ? <Moon size={20} /> : <Sun size={20} />}
        </IconButton>
        <label className="relative flex h-11 items-center gap-2 rounded-full border border-line bg-white px-4 text-sm font-extrabold text-ink shadow-sm">
          <Globe2 size={18} />
          <select
            aria-label="Langue"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
            className="appearance-none bg-transparent pr-6 font-extrabold outline-none"
          >
            <option value="fr">Français</option>
            <option value="en">English</option>
            <option value="ar">العربية</option>
            <option value="es">Español</option>
          </select>
          <ChevronDown className="pointer-events-none absolute right-3" size={16} />
        </label>
        <IconButton label="Compte">
          <UserCircle size={22} />
        </IconButton>
      </div>
    </header>
  );
}

function IconButton({ children, label, onClick }) {
  return (
    <button
      aria-label={label}
      title={label}
      onClick={onClick}
      className="grid size-11 place-items-center rounded-full border border-line bg-white text-ink shadow-sm"
    >
      {children}
    </button>
  );
}
