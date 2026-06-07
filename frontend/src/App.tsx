import ChatWindow from './components/ChatWindow';

export default function App() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <div className="mx-auto flex min-h-screen w-full max-w-5xl flex-col px-6 py-8">
        <header className="mb-6">
          <p className="text-sm font-medium uppercase tracking-wide text-slate-500">
            Day 1 Setup
          </p>
          <h1 className="mt-2 text-3xl font-semibold">
            AI Customer Support Agent
          </h1>
        </header>
        <ChatWindow />
      </div>
    </main>
  );
}
