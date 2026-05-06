import { createContext, useContext, useMemo, useState } from "react";

import { authApi } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("syncra_user") || "null"));

  async function persistSession(response) {
    const { user: nextUser, tokens } = response.data;
    localStorage.setItem("syncra_access", tokens.access);
    localStorage.setItem("syncra_refresh", tokens.refresh);
    localStorage.setItem("syncra_user", JSON.stringify(nextUser));
    setUser(nextUser);
  }

  async function login(payload) {
    await persistSession(await authApi.login(payload));
  }

  async function register(payload) {
    await persistSession(await authApi.register(payload));
  }

  function logout() {
    localStorage.removeItem("syncra_access");
    localStorage.removeItem("syncra_refresh");
    localStorage.removeItem("syncra_user");
    setUser(null);
  }

  const value = useMemo(() => ({ user, login, register, logout, isAuthenticated: Boolean(user) }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
