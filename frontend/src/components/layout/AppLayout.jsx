import { Bell, LogOut, MessageSquare, Settings, User } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";

const items = [
  ["Dashboard", "/dashboard", MessageSquare],
  ["Profile", "/profile", User],
  ["Settings", "/settings", Settings],
];

export function AppLayout() {
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen p-3 text-slate-100 md:p-6">
      <div className="mx-auto grid max-w-7xl gap-4 md:grid-cols-[17rem_1fr]">
        <aside className="glass rounded-lg p-4 shadow-glow">
          <div className="mb-8 flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-accent text-ink font-black">S</div>
            <div>
              <p className="text-lg font-semibold">Syncra</p>
              <p className="text-xs text-slate-400">{user?.username}</p>
            </div>
          </div>
          <nav className="grid gap-2">
            {items.map(([label, to, Icon]) => (
              <NavLink key={to} to={to} className={({ isActive }) => `flex items-center gap-3 rounded-md px-3 py-2 text-sm transition ${isActive ? "bg-white/10 text-white" : "text-slate-300 hover:bg-white/5"}`}>
                <Icon size={18} /> {label}
              </NavLink>
            ))}
          </nav>
          <button onClick={logout} className="mt-8 flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm text-slate-300 hover:bg-white/5">
            <LogOut size={18} /> Logout
          </button>
        </aside>
        <main className="glass min-h-[calc(100vh-3rem)] rounded-lg shadow-glow">
          <header className="flex items-center justify-between border-b border-white/10 px-5 py-4">
            <p className="font-medium">Real-time workspace</p>
            <button title="Notifications" className="rounded-md p-2 hover:bg-white/10"><Bell size={18} /></button>
          </header>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
