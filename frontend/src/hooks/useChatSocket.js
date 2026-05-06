import { useEffect, useRef, useState } from "react";

export function useChatSocket(chatId, onEvent) {
  const [connected, setConnected] = useState(false);
  const socketRef = useRef(null);
  const retryRef = useRef(0);

  useEffect(() => {
    if (!chatId) return undefined;
    let closedByEffect = false;
    const token = localStorage.getItem("syncra_access");

    function connect() {
      const ws = new WebSocket(`${import.meta.env.VITE_WS_URL}/chats/${chatId}/?token=${token}`);
      socketRef.current = ws;
      ws.onopen = () => {
        retryRef.current = 0;
        setConnected(true);
      };
      ws.onmessage = (event) => onEvent?.(JSON.parse(event.data));
      ws.onclose = () => {
        setConnected(false);
        if (!closedByEffect) {
          const delay = Math.min(1000 * 2 ** retryRef.current, 15000);
          retryRef.current += 1;
          setTimeout(connect, delay);
        }
      };
    }

    connect();
    return () => {
      closedByEffect = true;
      socketRef.current?.close();
    };
  }, [chatId, onEvent]);

  function send(event) {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(event));
    }
  }

  return { connected, send };
}
