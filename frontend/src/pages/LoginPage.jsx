import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

import { useAuth } from "../context/AuthContext";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    try {
      await login({ username: form.get("username"), password: form.get("password") });
      navigate("/dashboard");
    } catch {
      setError("Invalid username or password.");
    }
  }

  return (
    <main className="grid min-h-screen place-items-center p-4 text-slate-100">
      <form onSubmit={submit} className="glass w-full max-w-md rounded-lg p-6 shadow-glow">
        <h1 className="text-2xl font-semibold">Syncra</h1>
        <p className="mt-1 text-sm text-slate-400">Sign in to your real-time workspace.</p>
        {error && <p className="mt-4 rounded-md bg-flame/20 p-3 text-sm text-rose-100">{error}</p>}
        <input name="username" className="mt-6 w-full rounded-md border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-accent" placeholder="Username" />
        <input name="password" type="password" className="mt-3 w-full rounded-md border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-accent" placeholder="Password" />
        <button className="mt-5 w-full rounded-md bg-accent px-4 py-3 font-semibold text-ink">Login</button>
        <div className="mt-4 flex justify-between text-sm text-slate-400">
          <Link to="/register">Create account</Link>
          <Link to="/forgot-password">Forgot password?</Link>
        </div>
      </form>
    </main>
  );
}
