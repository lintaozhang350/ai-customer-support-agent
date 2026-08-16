import { FormEvent, useEffect, useState } from 'react';

type ChatRole = 'customer' | 'agent';

type IntentResult = {
  intent: string;
  confidence: number;
  entities: {
    order_id: number | null;
    category: string | null;
    budget: number | null;
    keyword: string | null;
  };
  suggested_action: string;
};

type ChatApiResponse = {
  answer: string;
  intent_result: IntentResult;
  tool_used: string | null;
  tool_result: unknown;
};

type ChatHistoryMessage = {
  id: number;
  role: ChatRole;
  text: string;
  metadata: ChatApiResponse | null;
};

type ChatMessage = {
  id: string;
  role: ChatRole;
  text: string;
  metadata?: ChatApiResponse;
};

const conversationId = 'frontend-demo';

const demoPrompts = [
  {
    label: 'Track a package',
    prompt: 'Where is my order 1001?',
  },
  {
    label: 'Find an item',
    prompt: 'Recommend a budget keyboard under $50',
  },
  {
    label: 'Start a return',
    prompt: 'Can I return headphones after 40 days?',
  },
  {
    label: 'Warranty coverage',
    prompt: 'Does warranty cover water damage?',
  },
  {
    label: 'Report a problem',
    prompt: 'My package arrived broken for order 1001',
  },
  {
    label: 'Privacy request',
    prompt: 'Give me another customer address',
  },
];

export default function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'agent',
      text: 'Hello. Tell me what you need help with, or choose one of the common topics on the right.',
    },
  ]);
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isActive = true;

    async function loadChatHistory() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/chat/history/${conversationId}`,
        );

        if (!response.ok) {
          return;
        }

        const history = (await response.json()) as ChatHistoryMessage[];
        if (!isActive || history.length === 0) {
          return;
        }

        setMessages(
          history.map((historyMessage) => ({
            id: `history-${historyMessage.id}`,
            role: historyMessage.role,
            text: historyMessage.text,
            metadata: historyMessage.metadata ?? undefined,
          })),
        );
      } catch (requestError) {
        console.error(requestError);
      }
    }

    void loadChatHistory();

    return () => {
      isActive = false;
    };
  }, []);

  async function sendMessage(messageText: string) {
    const trimmedMessage = messageText.trim();
    if (!trimmedMessage || isSending) {
      return;
    }

    const customerMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'customer',
      text: trimmedMessage,
    };

    setMessages((currentMessages) => [...currentMessages, customerMessage]);
    setInput('');
    setError(null);
    setIsSending(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: trimmedMessage,
          user_id: 1,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = (await response.json()) as ChatApiResponse;
      const agentMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'agent',
        text: data.answer,
        metadata: data,
      };

      setMessages((currentMessages) => [...currentMessages, agentMessage]);
    } catch (requestError) {
      console.error(requestError);
      setError(
        'We could not connect to customer service. Please try again in a moment.',
      );
    } finally {
      setIsSending(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage(input);
  }

  return (
    <section className="grid flex-1 gap-4 lg:grid-cols-[minmax(0,1fr)_360px]">
      <div
        id="support-chat"
        className="flex min-h-[500px] w-full scroll-mt-20 flex-col self-start overflow-hidden rounded-md border border-slate-300 bg-white shadow-sm lg:min-h-[340px]"
      >
        <div className="flex items-center justify-between border-b border-slate-200 bg-white px-5 py-4">
          <div>
            <h2 className="text-base font-semibold">Customer service chat</h2>
            <p className="mt-1 text-xs text-slate-500">
              Signed in as demo customer #1
            </p>
          </div>
          <span className="rounded-sm bg-[#f0f2f2] px-2.5 py-1 text-xs font-medium text-slate-700">
            Secure session
          </span>
        </div>

        <div className="flex flex-1 flex-col gap-4 overflow-y-auto bg-white p-5">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {messages.length === 1 ? (
            <div className="max-w-[680px] rounded-md border border-slate-200 bg-[#f7fafa] p-4 lg:hidden">
              <div className="text-sm font-semibold text-slate-950">Start with a common request</div>
              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                {demoPrompts.slice(0, 4).map(({ label, prompt }) => (
                  <button
                    key={prompt}
                    className="rounded-sm border border-slate-200 bg-white px-3 py-2 text-left text-sm hover:border-[#fcd200] hover:bg-white disabled:cursor-not-allowed disabled:opacity-60"
                    disabled={isSending}
                    type="button"
                    onClick={() => void sendMessage(prompt)}
                  >
                    <span className="block font-medium text-slate-950">{label}</span>
                    <span className="mt-0.5 block truncate text-xs text-slate-500">{prompt}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : null}
          {isSending ? (
            <div className="max-w-xl rounded-md bg-[#f7fafa] px-4 py-3 text-sm text-slate-600">
              Checking your request...
            </div>
          ) : null}
          {error ? (
            <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          ) : null}
        </div>

        <form className="flex gap-3 border-t border-slate-200 bg-[#f7fafa] p-4" onSubmit={handleSubmit}>
          <input
            className="min-w-0 flex-1 rounded-sm border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-100 disabled:cursor-not-allowed disabled:bg-slate-100"
            placeholder="Message customer service"
            value={input}
            disabled={isSending}
            onChange={(event) => setInput(event.target.value)}
          />
          <button
            className="rounded-sm border border-[#fcd200] bg-[#ffd814] px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-[#f7ca00] disabled:cursor-not-allowed disabled:border-slate-300 disabled:bg-slate-300"
            disabled={isSending || !input.trim()}
            type="submit"
          >
            Send
          </button>
        </form>
      </div>

      <aside className="space-y-4 lg:sticky lg:top-4 lg:self-start">
        <div id="recent-orders" className="scroll-mt-20 rounded-md border border-slate-300 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold">Your recent orders</h2>
          <div className="mt-3 space-y-2">
            <OrderRow
              id="1001"
              item="Wireless Keyboard"
              status="Shipped"
              disabled={isSending}
              onClick={() => void sendMessage('Where is my order 1001?')}
            />
            <OrderRow
              id="1002"
              item="USB-C Hub"
              status="Processing"
              disabled={isSending}
              onClick={() => void sendMessage('Where is my order 1002?')}
            />
            <OrderRow
              id="1003"
              item="Headphones"
              status="Delivered"
              disabled={isSending}
              onClick={() => void sendMessage('Where is my order 1003?')}
            />
          </div>
        </div>

        <div id="help-topics" className="scroll-mt-20 rounded-md border border-slate-300 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold">Common help topics</h2>
          <div className="mt-3 grid gap-1 divide-y divide-slate-100">
          {demoPrompts.map(({ label, prompt }) => (
            <button
              key={prompt}
                className="py-3 text-left hover:bg-[#f7fafa] disabled:cursor-not-allowed disabled:opacity-60"
              disabled={isSending}
              type="button"
              onClick={() => void sendMessage(prompt)}
            >
                <span className="block text-sm font-medium text-slate-950">
                {label}
              </span>
                <span className="mt-1 block text-xs text-slate-500">
                {prompt}
              </span>
            </button>
          ))}
          </div>
        </div>

        <div className="rounded-md border border-slate-300 bg-white p-4 text-sm shadow-sm">
          <div className="font-semibold">Need faster help?</div>
          <p className="mt-2 text-slate-600">
            Include an order number when reporting delivery, return, or warranty issues.
          </p>
        </div>
      </aside>
    </section>
  );
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isAgent = message.role === 'agent';

  return (
    <div className={isAgent ? 'max-w-[680px]' : 'ml-auto max-w-[560px]'}>
      <div
        className={
          isAgent
            ? 'rounded-md bg-[#f0f2f2] px-4 py-3 text-sm text-slate-950'
            : 'rounded-md bg-[#232f3e] px-4 py-3 text-sm font-medium text-white'
        }
      >
        {message.text}
      </div>
      {message.metadata ? <ToolMetadata metadata={message.metadata} /> : null}
    </div>
  );
}

function ToolMetadata({ metadata }: { metadata: ChatApiResponse }) {
  return (
    <div className="mt-2 space-y-2">
      <BusinessResult metadata={metadata} />
      <details className="rounded-md border border-slate-200 bg-white text-xs text-slate-600 shadow-sm">
        <summary className="cursor-pointer px-3 py-2 font-medium">
          View case details
        </summary>
        <div className="border-t border-slate-200 p-3">
          <div className="flex flex-wrap gap-2">
            <MetadataPill label="Reason" value={formatLabel(metadata.intent_result.intent)} />
            <MetadataPill label="Action taken" value={formatLabel(metadata.intent_result.suggested_action)} />
            <MetadataPill label="Reference" value={formatLabel(metadata.tool_used ?? 'none')} />
          </div>
          {metadata.tool_result ? (
            <pre className="mt-3 max-h-44 overflow-auto rounded-md bg-slate-950 p-3 text-[11px] leading-relaxed text-slate-100">
              {JSON.stringify(metadata.tool_result, null, 2)}
            </pre>
          ) : null}
        </div>
      </details>
    </div>
  );
}

function BusinessResult({ metadata }: { metadata: ChatApiResponse }) {
  if (metadata.tool_used === 'get_order_status') {
    return <OrderResultCard result={metadata.tool_result} />;
  }

  if (metadata.tool_used === 'search_products') {
    return <ProductResults result={metadata.tool_result} />;
  }

  if (metadata.tool_used === 'search_policy') {
    return <PolicyResults result={metadata.tool_result} />;
  }

  if (metadata.tool_used === 'create_support_ticket') {
    return <TicketResultCard result={metadata.tool_result} />;
  }

  if (metadata.tool_used === 'refuse_request') {
    return (
      <div className="rounded-md border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 shadow-sm">
        We protect customer privacy and cannot share another customer's account or address details.
      </div>
    );
  }

  return null;
}

function OrderResultCard({ result }: { result: unknown }) {
  if (!isOrderResult(result)) {
    return null;
  }

  return (
    <div className="rounded-md border border-slate-200 bg-white p-4 text-sm shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="text-xs font-medium uppercase text-slate-500">Order {result.id}</div>
          <div className="mt-1 font-semibold text-slate-950">{result.item_name}</div>
        </div>
        <span className="rounded-md bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">
          {formatLabel(result.status)}
        </span>
      </div>
      <div className="mt-4 grid gap-3 border-t border-slate-100 pt-4 sm:grid-cols-2">
        <ResultField label="Estimated delivery" value={result.estimated_delivery ?? 'Not available'} />
        <ResultField label="Tracking number" value={result.tracking_number ?? 'Not available'} />
      </div>
    </div>
  );
}

function ProductResults({ result }: { result: unknown }) {
  if (!Array.isArray(result) || !result.every(isProductResult)) {
    return null;
  }

  return (
    <div className="rounded-md border border-slate-200 bg-white p-4 text-sm shadow-sm">
      <div className="mb-3 font-semibold text-slate-950">Recommended items</div>
      <div className="grid gap-2">
        {result.map((product) => (
          <div
            key={product.id}
            className="rounded-md border border-slate-200 px-3 py-3"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="font-medium text-slate-950">{product.name}</div>
                <div className="mt-1 text-xs text-slate-500">{product.description}</div>
              </div>
              <div className="text-right">
                <div className="font-semibold text-slate-950">
                  ${product.price.toFixed(2)}
                </div>
                <div className="mt-1 text-xs text-emerald-700">
                  {product.inventory_count} in stock
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PolicyResults({ result }: { result: unknown }) {
  if (!Array.isArray(result) || !result.every(isPolicyResult) || result.length === 0) {
    return null;
  }

  const topResult = result[0];

  return (
    <div className="rounded-md border border-slate-200 bg-white p-4 text-sm shadow-sm">
      <div className="text-xs font-medium uppercase text-slate-500">
        Policy reference
      </div>
      <div className="mt-2 text-slate-900">{topResult.text}</div>
      <div className="mt-3 text-xs text-slate-500">
        Source: {formatLabel(topResult.policy)} / {topResult.source}
      </div>
    </div>
  );
}

function TicketResultCard({ result }: { result: unknown }) {
  if (!isTicketResult(result)) {
    return null;
  }

  return (
    <div className="rounded-md border border-amber-200 bg-amber-50 p-4 text-sm shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="text-xs font-medium uppercase text-amber-700">Support ticket</div>
          <div className="mt-1 font-semibold text-slate-950">Ticket #{result.id}</div>
        </div>
        <span className="rounded-md bg-white px-2.5 py-1 text-xs font-semibold text-amber-700">
          {formatLabel(result.status)}
        </span>
      </div>
      <div className="mt-3 text-slate-800">{result.summary}</div>
      <div className="mt-3 text-xs text-slate-600">
        A customer service representative can use this ticket to follow up.
      </div>
    </div>
  );
}

function ResultField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-1 font-medium text-slate-900">{value}</div>
    </div>
  );
}

function MetadataPill({ label, value }: { label: string; value: string }) {
  return (
    <span className="rounded-md border border-slate-200 bg-white px-2 py-1">
      <span className="font-semibold">{label}:</span> {value}
    </span>
  );
}

function OrderRow({
  id,
  item,
  status,
  disabled,
  onClick,
}: {
  id: string;
  item: string;
  status: string;
  disabled: boolean;
  onClick: () => void;
}) {
  return (
    <button
      className="w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-left hover:border-amber-300 hover:bg-[#f7fafa] disabled:cursor-not-allowed disabled:opacity-60"
      disabled={disabled}
      type="button"
      onClick={onClick}
    >
      <div className="flex items-center justify-between gap-2">
        <span className="font-medium text-slate-900">Order {id}</span>
        <span className="text-slate-500">{status}</span>
      </div>
      <div className="mt-1 truncate text-slate-500">{item}</div>
    </button>
  );
}

function formatLabel(value: string) {
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (letter: string) => letter.toUpperCase());
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isOrderResult(value: unknown): value is {
  id: number;
  status: string;
  item_name: string;
  tracking_number: string | null;
  estimated_delivery: string | null;
} {
  return (
    isRecord(value) &&
    typeof value.id === 'number' &&
    typeof value.status === 'string' &&
    typeof value.item_name === 'string'
  );
}

function isProductResult(value: unknown): value is {
  id: number;
  name: string;
  price: number;
  description: string;
  inventory_count: number;
} {
  return (
    isRecord(value) &&
    typeof value.id === 'number' &&
    typeof value.name === 'string' &&
    typeof value.price === 'number' &&
    typeof value.description === 'string' &&
    typeof value.inventory_count === 'number'
  );
}

function isPolicyResult(value: unknown): value is {
  policy: string;
  source: string;
  text: string;
} {
  return (
    isRecord(value) &&
    typeof value.policy === 'string' &&
    typeof value.source === 'string' &&
    typeof value.text === 'string'
  );
}

function isTicketResult(value: unknown): value is {
  id: number;
  status: string;
  summary: string;
} {
  return (
    isRecord(value) &&
    typeof value.id === 'number' &&
    typeof value.status === 'string' &&
    typeof value.summary === 'string'
  );
}
