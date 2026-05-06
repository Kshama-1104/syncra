import { Link } from "react-router-dom";

export function DashboardPage() {
  return (
    <section className="p-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <Link to="/chats" className="rounded-lg border border-white/10 bg-white/5 p-5 hover:bg-white/10">
          <p className="font-medium">Chats</p>
          <p className="mt-2 text-sm text-slate-400">Open direct and group conversations.</p>
        </Link>
        <div className="rounded-lg border border-white/10 bg-white/5 p-5">
          <p className="font-medium">Notifications</p>
          <p className="mt-2 text-sm text-slate-400">Unread activity and mentions.</p>
        </div>
        <div className="rounded-lg border border-white/10 bg-white/5 p-5">
          <p className="font-medium">Presence</p>
          <p className="mt-2 text-sm text-slate-400">Online, last seen, typing, and receipts.</p>
        </div>
      </div>
    </section>
  );
}
