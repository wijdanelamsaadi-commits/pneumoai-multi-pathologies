import { Outlet } from "react-router-dom";
import Header from "./Header.jsx";
import Sidebar from "./Sidebar.jsx";

export default function AppLayout() {
  return (
    <div className="app-shell min-h-screen bg-[radial-gradient(circle_at_top_left,#f9fbff_0,#ffffff_34%,#f7faff_100%)] text-ink">
      <Sidebar />
      <main className="lg:ml-[278px]">
        <div className="mx-auto max-w-[1180px] px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
          <Header />
          <Outlet />
        </div>
      </main>
    </div>
  );
}
