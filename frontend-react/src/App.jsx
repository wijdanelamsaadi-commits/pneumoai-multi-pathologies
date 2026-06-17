import { Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "./components/AppLayout.jsx";
import AboutPage from "./pages/AboutPage.jsx";
import AnalysisPage from "./pages/AnalysisPage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import ReportsPage from "./pages/ReportsPage.jsx";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="analyse" element={<AnalysisPage />} />
        <Route path="historique" element={<HistoryPage />} />
        <Route path="rapports" element={<ReportsPage />} />
        <Route path="a-propos" element={<AboutPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
