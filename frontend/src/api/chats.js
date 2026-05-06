import { api } from "./client";

export const chatsApi = {
  list: () => api.get("/chats/"),
  create: (payload) => api.post("/chats/", payload),
  messages: (chatId) => api.get(`/messages/?chat=${chatId}`),
  send: (chatId, body) => api.post(`/chats/${chatId}/messages/`, { body }),
  searchUsers: (q) => api.get(`/users/search/?search=${encodeURIComponent(q)}`),
};
