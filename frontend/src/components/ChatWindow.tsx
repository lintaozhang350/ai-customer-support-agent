const starterMessages = [
  {
    role: 'agent',
    text: 'Hi, I am your customer support assistant. The chat workflow will be connected in a later step.',
  },
  {
    role: 'customer',
    text: 'Where is my order 1001?',
  },
];

export default function ChatWindow() {
  return (
    <section className="flex flex-1 flex-col rounded-lg border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-5 py-4">
        <h2 className="text-lg font-semibold">Support Chat</h2>
      </div>
      <div className="flex flex-1 flex-col gap-4 p-5">
        {starterMessages.map((message) => (
          <div
            key={`${message.role}-${message.text}`}
            className={
              message.role === 'agent'
                ? 'max-w-xl rounded-lg bg-slate-100 px-4 py-3 text-sm'
                : 'ml-auto max-w-xl rounded-lg bg-blue-600 px-4 py-3 text-sm text-white'
            }
          >
            {message.text}
          </div>
        ))}
      </div>
      <form className="flex gap-3 border-t border-slate-200 p-4">
        <input
          className="min-w-0 flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          placeholder="Chat input placeholder"
          disabled
        />
        <button
          className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-60"
          disabled
        >
          Send
        </button>
      </form>
    </section>
  );
}
