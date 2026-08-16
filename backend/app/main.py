from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, orders, products

app = FastAPI(title="AI Customer Support Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Customer Support Agent API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
