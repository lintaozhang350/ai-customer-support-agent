# AI Customer Support Agent 项目讲解 Prompt

你是一位非常有耐心的编程老师。请假设我是初学者，帮我仔细讲解下面这个项目。

请用中文讲解，并按照以下要求来解释：

1. 先用大白话说明这个项目整体是做什么的。
2. 解释完整架构：前端、后端、配置文件、它们之间的关系。
3. 对每个文件说明：
   - 这个文件做什么
   - 为什么需要它
   - 它和其他文件怎么连接
   - 用到了什么技术
   - 如果删掉它会发生什么
4. 对每个源码文件展示完整代码。
5. 对每个源码文件逐行解释。
6. 最后告诉我下一步应该怎么继续开发 Day 2。

---

## 项目基本信息

项目名称：AI Customer Support Agent

GitHub 仓库：

```text
https://github.com/lintaozhang350/ai-customer-support-agent.git
```

当前分支：

```text
main
```

当前阶段：

```text
Day 1 setup
```

这个项目目前只是一个初始 full-stack scaffold，也就是项目骨架。

它已经包含：

- React + TypeScript + Tailwind 前端
- FastAPI 后端
- 一个占位聊天 UI
- 一个 backend health check API
- 未来开发 API、models、schemas、services、tools 的文件夹结构

它目前还没有实现：

- RAG
- OpenAI API 调用
- 数据库
- 真实聊天功能
- Agent workflow
- Tool calling
- 订单查询
- 商品推荐
- 转人工 ticket

---

## 当前项目架构

```text
Browser
  |
  v
frontend/index.html
  |
  v
frontend/src/main.tsx
  |
  v
frontend/src/App.tsx
  |
  v
frontend/src/components/ChatWindow.tsx

Backend, separately:
uvicorn app.main:app
  |
  v
backend/app/main.py
  |
  +-- GET /
  +-- GET /health
  +-- CORS allows frontend from http://localhost:5173
```

前端和后端目前是两个独立运行的部分。

前端现在还没有调用后端。

后端已经准备好接受 HTTP 请求。

---

## 项目文件结构

```text
ai-customer-support-agent/
|-- .gitignore
|-- README.md
|-- PROJECT_EXPLANATION_PROMPT.md
|-- frontend/
|   |-- index.html
|   |-- package.json
|   |-- postcss.config.js
|   |-- tailwind.config.ts
|   |-- tsconfig.json
|   |-- vite.config.ts
|   `-- src/
|       |-- App.tsx
|       |-- index.css
|       |-- main.tsx
|       `-- components/
|           `-- ChatWindow.tsx
`-- backend/
    |-- requirements.txt
    |-- app/
    |   |-- __init__.py
    |   |-- main.py
    |   |-- api/
    |   |   `-- __init__.py
    |   |-- core/
    |   |   `-- __init__.py
    |   |-- models/
    |   |   `-- __init__.py
    |   |-- schemas/
    |   |   `-- __init__.py
    |   |-- services/
    |   |   `-- __init__.py
    |   `-- tools/
    |       `-- __init__.py
    `-- tests/
        `-- __init__.py
```

---

## 每个文件的作用总结

| File | What it does | Why it exists | Connects to | Tech | If removed |
|---|---|---|---|---|---|
| `.gitignore` | Tells Git what not to track | Keeps generated files out of repo | Git | Git | `node_modules`, `.venv`, caches may pollute commits |
| `README.md` | Explains project and run steps | Helps users/reviewers understand the project | Whole repo | Markdown | Project becomes harder to understand |
| `backend/requirements.txt` | Lists Python packages | Lets backend install dependencies | `backend/app/main.py` | Python/FastAPI | Backend dependencies are unclear |
| `backend/app/main.py` | Creates FastAPI app and routes | Backend entry point | Uvicorn, frontend CORS | FastAPI | Backend cannot start |
| `backend/app/__init__.py` | Marks `app` as Python package | Allows imports like `app.main` | Uvicorn | Python | Imports may fail |
| `backend/app/api/__init__.py` | Placeholder package for routes | Future API organization | Future routers | Python | No immediate break |
| `backend/app/core/__init__.py` | Placeholder for settings/config | Future app config | Future settings | Python | No immediate break |
| `backend/app/models/__init__.py` | Placeholder for DB models | Future database tables | Future ORM | Python | No immediate break |
| `backend/app/schemas/__init__.py` | Placeholder for request/response schemas | Future validation | Pydantic | Python | No immediate break |
| `backend/app/services/__init__.py` | Placeholder for business logic | Future reusable logic | API/tools | Python | No immediate break |
| `backend/app/tools/__init__.py` | Placeholder for agent tools | Future order/product tools | Agent workflow | Python | No immediate break |
| `backend/tests/__init__.py` | Marks tests as package | Future backend tests | Pytest | Python | Tests may still work, but less structured |
| `frontend/package.json` | Defines frontend dependencies/scripts | Lets you run/build React app | Vite/npm | Node/React | Frontend cannot install/run cleanly |
| `frontend/index.html` | HTML shell for React | Gives React a root DOM node | `main.tsx` | HTML/Vite | Frontend cannot mount |
| `frontend/vite.config.ts` | Vite config | Enables React plugin and port | npm scripts | Vite | Dev server may not use React setup |
| `frontend/tsconfig.json` | TypeScript rules | Controls TS checking | TS compiler | TypeScript | Build/type checking may fail |
| `frontend/tailwind.config.ts` | Tailwind scan config | Tells Tailwind where classes live | CSS build | Tailwind | Styling classes may not generate |
| `frontend/postcss.config.js` | CSS processor config | Runs Tailwind and autoprefixer | `index.css` | PostCSS | Tailwind CSS may not compile |
| `frontend/src/main.tsx` | React entry point | Mounts app into HTML | `App.tsx`, `index.html` | React/TS | UI will not render |
| `frontend/src/App.tsx` | Main app layout | Top-level screen | `ChatWindow.tsx` | React/Tailwind | App has no visible layout |
| `frontend/src/components/ChatWindow.tsx` | Placeholder chat UI | Shows future chat shape | `App.tsx` | React/Tailwind | Chat area disappears |
| `frontend/src/index.css` | Loads Tailwind CSS | Enables Tailwind styling | `main.tsx` | CSS/Tailwind | Styling mostly disappears |

---

## Source File: backend/app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Customer Support Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Customer Support Agent API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

请逐行解释这个文件。

---

## Source File: frontend/src/main.tsx

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

请逐行解释这个文件。

---

## Source File: frontend/src/App.tsx

```tsx
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
```

请逐行解释这个文件。

---

## Source File: frontend/src/components/ChatWindow.tsx

```tsx
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
```

请逐行解释这个文件。

---

## Source File: frontend/src/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
}
```

请逐行解释这个文件。

---

## Config File: frontend/package.json

```json
{
  "name": "ai-customer-support-agent-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.18",
    "@types/react-dom": "^18.3.5",
    "@vitejs/plugin-react": "^4.3.4",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "typescript": "^5.6.3",
    "vite": "^5.4.11"
  }
}
```

请逐行解释这个配置文件，尤其解释：

- dependencies 和 devDependencies 的区别
- npm run dev 做了什么
- npm run build 做了什么
- React、Vite、TypeScript、Tailwind 分别负责什么

---

## Config File: frontend/index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Customer Support Agent</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

请逐行解释这个文件，并说明 React 是怎么挂载到 `root` 上的。

---

## Config File: frontend/vite.config.ts

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
```

请逐行解释这个文件。

---

## Config File: frontend/tailwind.config.ts

```ts
import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
} satisfies Config;
```

请逐行解释这个文件，并说明 Tailwind 为什么需要 `content`。

---

## Config File: frontend/postcss.config.js

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

请逐行解释这个文件，并说明 PostCSS 和 Autoprefixer 的作用。

---

## Config File: frontend/tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": []
}
```

请逐行解释这个 TypeScript 配置文件，用初学者能听懂的话说明每个选项大概控制什么。

---

## Config File: backend/requirements.txt

```text
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic==2.10.4
```

请逐行解释：

- FastAPI 是什么
- Uvicorn 是什么
- Pydantic 是什么
- 为什么后端需要它们

---

## Config File: .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
.pytest_cache/

# Node
node_modules/
dist/
.vite/

# Environment
.env
.env.local

# OS / editor
.DS_Store
Thumbs.db
.vscode/
.idea/
```

请逐行解释这个文件，并说明为什么这些文件夹或文件不应该提交到 GitHub。

---

## Empty Python Package Files

这些文件目前是空的：

```text
backend/app/__init__.py
backend/app/api/__init__.py
backend/app/core/__init__.py
backend/app/models/__init__.py
backend/app/schemas/__init__.py
backend/app/services/__init__.py
backend/app/tools/__init__.py
backend/tests/__init__.py
```

请解释：

1. 为什么 Python 项目里经常有 `__init__.py`
2. 为什么这些文件现在是空的
3. 未来每个文件夹会放什么
4. 如果删除这些文件，会不会马上出问题

---

## 请最后回答

请在最后给我一个学习路线：

1. 我应该先理解哪些文件
2. 哪些文件只是配置，暂时不用深究
3. Day 2 应该怎么继续开发
4. 如何把前端输入框连接到后端
5. 如何逐步把这个项目变成真正的 AI Customer Support Agent
