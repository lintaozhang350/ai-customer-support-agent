# AI Customer Support Agent

A full-stack starter project for an AI customer support agent using React, FastAPI, RAG, and tool calling concepts. This repository is currently in the early MVP stage: project structure, frontend scaffold, backend scaffold, mock data, and basic API routes.

## Current Scope

- React + TypeScript + Tailwind frontend folder
- FastAPI backend folder
- Basic health-check API
- Placeholder chat UI
- Mock order and product data
- Order lookup API
- Product search API
- Rule-based intent classification API
- Basic tool execution for order lookup and product search inside `/api/chat`
- Local policy retrieval for return, shipping, and warranty questions
- No vector database, LLM tool calling, or advanced agent workflow implemented yet

## Project Structure

```text
ai-customer-support-agent/
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |   `-- ChatWindow.tsx
|   |   |-- App.tsx
|   |   |-- index.css
|   |   `-- main.tsx
|   |-- index.html
|   |-- package.json
|   |-- postcss.config.js
|   |-- tailwind.config.ts
|   |-- tsconfig.json
|   `-- vite.config.ts
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |-- core/
|   |   |-- models/
|   |   |-- schemas/
|   |   |-- services/
|   |   |-- tools/
|   |   `-- main.py
|   |-- tests/
|   `-- requirements.txt
`-- README.md
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server will run on `http://localhost:5173`.

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend API will run on `http://localhost:8000`.

Health check:

```text
GET http://localhost:8000/health
```

Order lookup:

```text
GET http://localhost:8000/api/orders/1001
```

Product search:

```text
GET http://localhost:8000/api/products/search?category=keyboard&budget=50
```

Chat intent classification:
Chat endpoint:

```text
POST http://localhost:8000/api/chat
Body: {"message": "Where is my order 1001?", "user_id": 1}
```

For order and product questions, `/api/chat` now calls the matching mock-data tool and includes `tool_used` plus `tool_result` in the response.
For return, shipping, and warranty questions, `/api/chat` retrieves relevant chunks from local policy text files in `backend/knowledge_base` and includes source metadata in `tool_result`.

## Next Steps

- Replace keyword policy search with vector RAG
- Add support ticket creation
- Connect the frontend chat input to `/api/chat`
