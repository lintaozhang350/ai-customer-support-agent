import ChatWindow from './components/ChatWindow';

export default function App() {
  return (
    <main className="min-h-screen bg-[#eaeded] text-slate-950">
      <header className="border-b border-slate-300 bg-[#131921] text-white">
        <div className="mx-auto flex w-full max-w-7xl items-center gap-4 px-4 py-3 sm:px-6 lg:px-8">
          <div className="shrink-0">
            <div className="text-lg font-bold leading-none">ShopDesk</div>
            <div className="mt-0.5 text-[11px] text-slate-300">Customer Service</div>
          </div>
          <label className="hidden min-w-0 flex-1 sm:block">
            <span className="sr-only">Search customer service</span>
            <input
              className="w-full rounded-md border-0 bg-white px-4 py-2 text-sm text-slate-900 outline-none placeholder:text-slate-500 focus:ring-2 focus:ring-amber-300"
              placeholder="Search orders, returns, warranty, or products"
              type="search"
            />
          </label>
          <nav className="ml-auto flex items-center gap-4 text-sm text-slate-200">
            <a className="hidden hover:text-white sm:inline" href="#recent-orders">Orders</a>
            <a className="hidden hover:text-white sm:inline" href="#help-topics">Returns</a>
            <a className="hover:text-white" href="#support-chat">Help</a>
            <a
              className="rounded-sm border border-slate-500 px-2 py-1 text-xs hover:border-slate-300 hover:text-white"
              href="#support-chat"
            >
              Account
            </a>
          </nav>
        </div>
      </header>

      <div className="mx-auto flex min-h-[calc(100vh-57px)] w-full max-w-7xl flex-col px-4 py-5 sm:px-6 lg:px-8">
        <header className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="text-sm text-slate-600">Help Center</div>
            <h1 className="mt-1 text-2xl font-semibold text-slate-950">
              Get help with your order
            </h1>
            <p className="mt-1 text-sm text-slate-600">
              Message customer service about delivery, returns, warranty coverage, or product recommendations.
            </p>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-600">
            <span className="h-2 w-2 rounded-full bg-emerald-500" aria-hidden="true" />
            Customer service is online
          </div>
        </header>
        <ChatWindow />
      </div>
    </main>
  );
}
