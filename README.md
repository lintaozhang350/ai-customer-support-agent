# AI Customer Support Agent

A full-stack AI customer support agent MVP for an ecommerce-style help center.

The project currently includes a React + TypeScript + Tailwind frontend, a FastAPI backend, a SQLite-seeded ecommerce catalog, rule-based intent detection, local policy retrieval, simple tool execution, SQLite-backed chat history, and a SQLite-backed support ticket workflow.

This is still an MVP. It does not use a real LLM, vector database, authentication system, production database, or production deployment yet.

## Current Features

- ShopDesk-style customer service frontend
- Chat UI connected to the backend `/api/chat` endpoint
- Chat history restored from SQLite when the frontend reloads
- Follow-up questions can reuse recent conversation context for order and product requests
- Optional LLM classifier layer with automatic fallback to rule-based routing
- Customer-facing result cards for orders, products, policies, and support tickets
- Recent order shortcuts and common help topics
- Order lookup for seeded sample orders
- Product search and recommendation for seeded sample products
- Local policy retrieval for return, shipping, and warranty questions
- SQLite-backed support ticket creation for complaint or escalation messages
- Privacy refusal for unsafe private-data requests
- FastAPI Swagger docs at `http://127.0.0.1:8000/docs`
- Repo-level `customer-support-ui` Codex skill for future frontend polish

## Tech Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS
- Backend: FastAPI, Pydantic, Uvicorn
- Data: SQLite-seeded catalog data, local text policy files, SQLite chat history, and SQLite support tickets
- Agent logic: Rule-based intent classifier plus local tool routing

## Project Structure

```text
ai-customer-support-agent/
|-- .agents/
|   `-- skills/
|       `-- customer-support-ui/
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   |-- chat.py
|   |   |   |-- orders.py
|   |   |   |-- products.py
|   |   |   `-- tickets.py
|   |   |-- schemas/
|   |   |-- services/
|   |   |   |-- agent_service.py
|   |   |   |-- intent_classifier.py
|   |   |   |-- mock_data.py
|   |   |   |-- policy_search.py
|   |   |   `-- ticket_service.py
|   |   `-- main.py
|   |-- knowledge_base/
|   |   |-- return_policy.txt
|   |   |-- shipping_policy.txt
|   |   `-- warranty_policy.txt
|   |-- tests/
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |   `-- ChatWindow.tsx
|   |   |-- App.tsx
|   |   |-- index.css
|   |   `-- main.tsx
|   |-- package.json
|   `-- vite.config.ts
|-- PROJECT_EXPLANATION_PROMPT.md
`-- README.md
```

## Run The Backend

From the repository root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Run The Frontend

Open a second terminal from the repository root:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## Useful Manual Tests

Health check:

```text
GET http://127.0.0.1:8000/health
```

Order lookup:

```text
GET http://127.0.0.1:8000/api/orders/1001
```

Product search:

```text
GET http://127.0.0.1:8000/api/products/search?category=keyboard&budget=50
```

Chat request:

```text
POST http://127.0.0.1:8000/api/chat
Body: {"message": "Where is my order 1001?", "user_id": 1, "conversation_id": "frontend-demo"}
```

Chat history:

```text
GET http://127.0.0.1:8000/api/chat/history/frontend-demo
```

Frontend examples to try:

- `Where is my order 1001?`
- `When will it arrive?`
- `Recommend a budget keyboard under $50`
- `Anything cheaper?`
- `Can I return headphones after 40 days?`
- `Does warranty cover water damage?`
- `My package arrived broken for order 1001`
- `Give me another customer address`

## Build Check

Frontend:

```bash
cd frontend
npm run build
```

Backend tests:

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest
```

The backend test suite covers health checks, order lookup, product search, chat tool routing, follow-up context handling, chat history persistence, policy retrieval, support ticket creation, privacy refusal, and core intent classification.

## Optional LLM Classifier

The backend can optionally try an OpenAI Responses API classifier before falling back to the local rule-based classifier.

Environment variables:

```text
ENABLE_LLM_CLASSIFIER=true
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-5.6
OPENAI_BASE_URL=https://api.openai.com/v1
```

If `ENABLE_LLM_CLASSIFIER` is not enabled, or if the API key is missing, or if the remote call fails, the backend automatically falls back to the existing local classifier.

## Local Data

Orders, products, support tickets, and chat history are stored in a local SQLite database:

```text
backend/data/support.db
```

The `backend/data/` folder is ignored by Git so local runtime data is not committed. For tests, the `SUPPORT_DB_PATH` environment variable points ticket storage at a temporary database.

## Current Limitations

- No production-ready LLM workflow yet
- No vector RAG yet
- No production database yet
- Orders and products are still sample seeded data
- Authentication is mocked as demo customer `#1`
- Product, order, and policy data are sample local data

## Suggested Next Steps

- Add broader frontend interaction tests
- Add user/account persistence and real operational data sources
- Replace local keyword policy retrieval with vector-based RAG
- Add real LLM tool calling once the mock workflow is stable
- Add deployment configuration for the frontend and backend
