import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  async function submit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await register({
      username: form.get("username"),
      email: form.get("email"),
      password: form.get("password"),
    });
    navigate("/dashboard");
  }

  return (
    <main className="grid min-h-screen place-items-center p-4 text-slate-100">
      <form onSubmit={submit} className="glass w-full max-w-md rounded-lg p-6 shadow-glow">
        <h1 className="text-2xl font-semibold">Create Syncra account</h1>
        <input name="username" className="mt-6 w-full rounded-md border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-accent" placeholder="Username" />
        <input name="email" type="email" className="mt-3 w-full rounded-md border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-accent" placeholder="Email" />
        <input name="password" type="password" className="mt-3 w-full rounded-md border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-accent" placeholder="Password" />
        <button className="mt-5 w-full rounded-md bg-accent px-4 py-3 font-semibold text-ink">Register</button>
        <Link className="mt-4 block text-sm text-slate-400" to="/login">Already have an account?</Link>
      </form>
    </main>
  );
}
