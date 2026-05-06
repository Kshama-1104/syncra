import { Send } from "lucide-react";
import { useState } from "react";

export function MessageThread({ messages, connected, onSend }) {
  const [body, setBody] = useState("");

  function submit(event) {
    event.preventDefault();
    if (!body.trim()) return;
    onSend(body.trim());
    setBody("");
  }

  return (
    <section className="grid min-h-[70vh] grid-rows-[1fr_auto]">
      <div className="flex flex-col-reverse gap-3 overflow-y-auto p-5">
        {[...messages].reverse().map((message) => (
          <div key={message.id} className="max-w-[75%] rounded-lg bg-white/10 px-4 py-3">
            <p className="text-sm">{message.body}</p>
            <p className="mt-1 text-[11px] text-slate-400">{message.sender?.username || `user:${message.sender_id}`}</p>
          </div>
        ))}
      </div>
      <form onSubmit={submit} className="flex gap-3 border-t border-white/10 p-4">
        <input value={body} onChange={(event) => setBody(event.target.value)} className="flex-1 rounded-md border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-accent" placeholder={connected ? "Message Syncra" : "Reconnecting..."} />
        <button className="rounded-md bg-accent px-4 text-ink transition hover:bg-teal-300" title="Send"><Send size={18} /></button>
      </form>
    </section>
  );
}
