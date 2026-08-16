# AI Customer Support Agent

A full-stack AI customer support agent MVP for an ecommerce-style help center.

The project currently includes a React + TypeScript + Tailwind frontend, a FastAPI backend, mock ecommerce data, rule-based intent detection, local policy retrieval, simple tool execution, and a SQLite-backed support ticket workflow.

This is still an MVP. It does not use a real LLM, vector database, authentication system, production database, or production deployment yet.

## Current Features

- ShopDesk-style customer service frontend
- Chat UI connected to the backend `/api/chat` endpoint
- Customer-facing result cards for orders, products, policies, and support tickets
- Recent order shortcuts and common help topics
- Order lookup for mock orders
- Product search and recommendation for mock products
- Local policy retrieval for return, shipping, and warranty questions
- SQLite-backed support ticket creation for complaint or escalation messages
- Privacy refusal for unsafe private-data requests
- FastAPI Swagger docs at `http://127.0.0.1:8000/docs`
- Repo-level `customer-support-ui` Codex skill for future frontend polish

## Tech Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS
- Backend: FastAPI, Pydantic, Uvicorn
- Data: In-memory mock ecommerce data, local text policy files, and SQLite support tickets
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
Body: {"message": "Where is my order 1001?", "user_id": 1}
```

Frontend examples to try:

- `Where is my order 1001?`
- `Recommend a budget keyboard under $50`
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

The backend test suite covers health checks, order lookup, product search, chat tool routing, policy retrieval, support ticket creation, privacy refusal, and core intent classification.

## Local Data

Support tickets are stored in a local SQLite database:

```text
backend/data/support.db
```

The `backend/data/` folder is ignored by Git so local runtime data is not committed. For tests, the `SUPPORT_DB_PATH` environment variable points ticket storage at a temporary database.

## Current Limitations

- No real LLM integration yet
- No vector RAG yet
- No production database yet
- Orders and products are still sample in-memory data
- Authentication is mocked as demo customer `#1`
- Product, order, and policy data are sample local data

## Suggested Next Steps

- Add broader frontend interaction tests
- Add persistent storage for orders, products, and conversations
- Replace local keyword policy retrieval with vector-based RAG
- Add real LLM tool calling once the mock workflow is stable
- Add deployment configuration for the frontend and backend
