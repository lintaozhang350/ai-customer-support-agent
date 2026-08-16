from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, orders, products, tickets
from app.core.settings import get_settings

settings = get_settings()

app = FastAPI(title="AI Customer Support Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(tickets.router, prefix="/api")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Customer Support Agent API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
