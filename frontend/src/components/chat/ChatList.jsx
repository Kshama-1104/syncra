import { MessageCircle } from "lucide-react";

export function ChatList({ chats, activeId, onSelect }) {
  return (
    <div className="border-r border-white/10">
      <div className="border-b border-white/10 p-4">
        <input className="w-full rounded-md border border-white/10 bg-white/5 px-3 py-2 text-sm outline-none focus:border-accent" placeholder="Search chats" />
      </div>
      <div className="max-h-[70vh] overflow-y-auto">
        {chats.map((chat) => (
          <button key={chat.id} onClick={() => onSelect(chat.id)} className={`flex w-full items-center gap-3 border-b border-white/5 p-4 text-left hover:bg-white/5 ${String(activeId) === String(chat.id) ? "bg-white/10" : ""}`}>
            <span className="grid h-10 w-10 place-items-center rounded-lg bg-accent/20 text-accent"><MessageCircle size={18} /></span>
            <span className="min-w-0">
              <span className="block truncate text-sm font-medium">{chat.title || `Chat ${chat.id}`}</span>
              <span className="block truncate text-xs text-slate-400">{chat.last_message?.body || "No messages yet"}</span>
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
