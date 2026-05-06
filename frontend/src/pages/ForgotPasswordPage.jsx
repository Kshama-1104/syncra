export function ForgotPasswordPage() {
  return (
    <main className="grid min-h-screen place-items-center p-4 text-slate-100">
      <form className="glass w-full max-w-md rounded-lg p-6 shadow-glow">
        <h1 className="text-2xl font-semibold">Reset password</h1>
        <input className="mt-6 w-full rounded-md border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-accent" placeholder="Email address" />
        <button className="mt-5 w-full rounded-md bg-accent px-4 py-3 font-semibold text-ink">Send reset link</button>
      </form>
    </main>
  );
}
