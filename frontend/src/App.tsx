import { FormEvent, useEffect, useState } from 'react';

import ChatWindow, { type SupportUiAction } from './components/ChatWindow';

export default function App() {
  const [uiAction, setUiAction] = useState<SupportUiAction | null>(null);
  const [isAccountPanelOpen, setIsAccountPanelOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  function triggerUiAction(action: Omit<SupportUiAction, 'id'>) {
    setUiAction({
      id: crypto.randomUUID(),
      ...action,
    });
  }

  useEffect(() => {
    if (!isAccountPanelOpen) {
      return;
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        setIsAccountPanelOpen(false);
      }
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isAccountPanelOpen]);

  function handleHeaderSearchSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuery = searchQuery.trim();
    if (!trimmedQuery) {
      triggerUiAction({ type: 'focus-composer', targetId: 'support-chat' });
      return;
    }

    triggerUiAction({
      type: 'send-prompt',
      prompt: trimmedQuery,
      targetId: 'support-chat',
    });
    setSearchQuery('');
  }

  return (
    <main className="min-h-screen bg-[#eaeded] text-slate-950">
      <header className="border-b border-slate-300 bg-[#131921] text-white">
        <div className="mx-auto flex w-full max-w-7xl items-center gap-4 px-4 py-3 sm:px-6 lg:px-8">
          <div className="shrink-0">
            <div className="text-lg font-bold leading-none">ShopDesk</div>
            <div className="mt-0.5 text-[11px] text-slate-300">Customer Service</div>
          </div>
          <form className="hidden min-w-0 flex-1 sm:block" onSubmit={handleHeaderSearchSubmit}>
            <label>
              <span className="sr-only">Search customer service</span>
              <input
                className="w-full rounded-md border-0 bg-white px-4 py-2 text-sm text-slate-900 outline-none placeholder:text-slate-500 focus:ring-2 focus:ring-amber-300"
                placeholder="Search orders, returns, warranty, or products"
                type="search"
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
              />
            </label>
          </form>
          <nav className="ml-auto flex items-center gap-4 text-sm text-slate-200">
            <button
              className="hidden hover:text-white sm:inline"
              type="button"
              onClick={() => triggerUiAction({ type: 'scroll', targetId: 'recent-orders' })}
            >
              Orders
            </button>
            <button
              className="hidden hover:text-white sm:inline"
              type="button"
              onClick={() =>
                triggerUiAction({
                  type: 'prefill-input',
                  prompt: 'Can I return headphones after 40 days?',
                  targetId: 'support-chat',
                })
              }
            >
              Returns
            </button>
            <button
              className="hover:text-white"
              type="button"
              onClick={() => triggerUiAction({ type: 'focus-composer', targetId: 'support-chat' })}
            >
              Help
            </button>
            <button
              className="rounded-sm border border-slate-500 px-2 py-1 text-xs hover:border-slate-300 hover:text-white"
              type="button"
              onClick={() => setIsAccountPanelOpen(true)}
            >
              Account
            </button>
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
        <ChatWindow uiAction={uiAction} />
      </div>

      {isAccountPanelOpen ? (
        <div
          className="fixed inset-0 z-50 flex items-start justify-center bg-slate-950/40 px-4 py-10"
          role="dialog"
          aria-modal="true"
          aria-labelledby="account-panel-title"
          onClick={() => setIsAccountPanelOpen(false)}
        >
          <div
            className="w-full max-w-lg rounded-md border border-slate-200 bg-white shadow-xl"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-4 border-b border-slate-200 px-5 py-4">
              <div>
                <div className="text-xs font-medium uppercase tracking-wide text-slate-500">
                  Account
                </div>
                <h2 id="account-panel-title" className="mt-1 text-lg font-semibold text-slate-950">
                  Demo customer profile
                </h2>
              </div>
              <button
                className="rounded-sm border border-slate-300 px-2 py-1 text-xs font-medium text-slate-700 hover:bg-slate-50"
                type="button"
                onClick={() => setIsAccountPanelOpen(false)}
              >
                Close
              </button>
            </div>

            <div className="space-y-4 px-5 py-4 text-sm">
              <div className="grid gap-3 sm:grid-cols-2">
                <InfoBlock label="Signed in as" value="Demo customer #1" />
                <InfoBlock label="Support status" value="Customer service is online" />
                <InfoBlock label="Recent order" value="Order 1001 - Wireless Keyboard" />
                <InfoBlock label="Preferred help" value="Orders, returns, warranty" />
              </div>

              <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
                <div className="font-medium text-slate-950">Quick account actions</div>
                <div className="mt-3 flex flex-wrap gap-2">
                  <button
                    className="rounded-sm border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 hover:border-slate-400 hover:bg-slate-50"
                    type="button"
                    onClick={() => {
                      triggerUiAction({ type: 'send-prompt', prompt: 'Where is my order 1001?', targetId: 'support-chat' });
                      setIsAccountPanelOpen(false);
                    }}
                  >
                    Check recent order
                  </button>
                  <button
                    className="rounded-sm border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 hover:border-slate-400 hover:bg-slate-50"
                    type="button"
                    onClick={() => {
                      triggerUiAction({ type: 'send-prompt', prompt: 'Can I return headphones after 40 days?', targetId: 'support-chat' });
                      setIsAccountPanelOpen(false);
                    }}
                  >
                    Ask about returns
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </main>
  );
}

function InfoBlock({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-slate-200 bg-white p-3">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-1 font-medium text-slate-950">{value}</div>
    </div>
  );
}
