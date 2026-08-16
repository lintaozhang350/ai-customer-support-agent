# AI Customer Support Agent

Small full-stack customer support demo for an ecommerce store.

The app has a React frontend and a FastAPI backend. It can answer common support questions, look up sample orders, recommend products from a small catalog, search return/shipping/warranty policy text, and create support tickets for damaged-order complaints.

## What it does

- chat UI for customer support
- order lookup
- product recommendations
- return, shipping, and warranty policy answers
- support ticket creation for complaints or escalation requests
- chat history and recent conversations
- basic follow-up handling, for example:
  - `Where is my order 1001?`
  - `When will it arrive?`
- refusal for unsafe requests like another customer's address

There is also optional OpenAI support for:

- intent classification
- answer rewriting

If that is not enabled, the app falls back to the local rule-based flow.

## Stack

- frontend: React, TypeScript, Vite, Tailwind CSS
- backend: FastAPI, Pydantic, Uvicorn
- data: SQLite
- tests: pytest, Playwright

## Project layout

```text
frontend/   React app
backend/    FastAPI app
e2e/        Playwright tests
```

The main frontend code lives in `frontend/src/components/ChatWindow.tsx`.

The main backend flow lives in:

- `backend/app/api/chat.py`
- `backend/app/services/agent_service.py`
- `backend/app/services/intent_classifier.py`
- `backend/app/services/mock_data.py`

## Running locally

### Backend

From the repo root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://127.0.0.1:5173
```

### Root scripts

You can also start from the repo root:

```bash
npm run backend:dev
npm run frontend:dev
```

## Useful test prompts

- `Where is my order 1001?`
- `When will it arrive?`
- `Recommend a budget keyboard under $50`
- `Anything cheaper?`
- `Can I return headphones after 40 days?`
- `Does warranty cover water damage?`
- `My package arrived broken for order 1001`
- `Give me another customer address`
- `Who are you?`

## Testing

Backend tests:

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest
```

Frontend build:

```bash
cd frontend
npm run build
```

Playwright:

```bash
npm run test:e2e
```

As of August 16, 2026, the local checks were:

- backend tests passing
- frontend build passing
- Playwright order lookup and follow-up tests passing

## Optional OpenAI setup

Create a local `.env.local` file and set:

```text
ENABLE_LLM_CLASSIFIER=true
ENABLE_LLM_ANSWER_GENERATION=true
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-5.6
OPENAI_BASE_URL=https://api.openai.com/v1
```

Without these settings, the backend uses the local logic only.

## Notes

- sample orders and products are seeded into `backend/data/support.db`
- the project uses demo customer data only
- there is no auth flow yet
- there is no RAG pipeline yet
- this is not production-deployed
