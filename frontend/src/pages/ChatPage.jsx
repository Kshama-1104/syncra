import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { chatsApi } from "../api/chats";
import { ChatList } from "../components/chat/ChatList";
import { MessageThread } from "../components/chat/MessageThread";
import { useChatSocket } from "../hooks/useChatSocket";

export function ChatPage() {
  const { chatId } = useParams();
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    chatsApi.list().then(({ data }) => setChats(data.results || data));
  }, []);

  useEffect(() => {
    if (chatId) chatsApi.messages(chatId).then(({ data }) => setMessages(data.results || data));
  }, [chatId]);

  const onEvent = useCallback((event) => {
    if (event.type === "message.created") {
      setMessages((current) => [{ id: event.message_id, body: event.body, sender_id: event.sender_id }, ...current]);
    }
  }, []);

  const { connected, send } = useChatSocket(chatId, onEvent);

  function sendMessage(body) {
    send({ type: "message.send", body });
  }

  return (
    <div className="grid md:grid-cols-[20rem_1fr]">
      <ChatList chats={chats} activeId={chatId} onSelect={(id) => navigate(`/chats/${id}`)} />
      {chatId ? <MessageThread messages={messages} connected={connected} onSend={sendMessage} /> : <div className="grid min-h-[70vh] place-items-center text-slate-400">Select a chat</div>}
    </div>
  );
}
