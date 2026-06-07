# AI Customer Support Agent

A full-stack starter project for an AI customer support agent using React, FastAPI, RAG, and tool calling concepts. This repository is currently at the Day 1 setup stage: project structure, frontend scaffold, backend scaffold, and basic run instructions.

## Day 1 Scope

- React + TypeScript + Tailwind frontend folder
- FastAPI backend folder
- Basic health-check API
- Placeholder chat UI
- No RAG, vector database, tool calling, or agent workflow implemented yet

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

## Next Steps

- Day 2: Add mock order and product data
- Day 3: Add intent classification
- Day 4: Add simple backend tools for order and product lookup
- Day 5+: Add policy search and RAG
