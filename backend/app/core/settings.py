import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env.local"
BACKEND_ENV_FILE = Path(__file__).resolve().parents[2] / ".env.local"

load_dotenv(ROOT_ENV_FILE)
load_dotenv(BACKEND_ENV_FILE)


@dataclass(frozen=True)
class Settings:
    enable_llm_classifier: bool
    enable_llm_answer_generation: bool
    openai_api_key: str | None
    openai_model: str
    openai_base_url: str
    cors_origins: list[str]


def get_settings() -> Settings:
    return Settings(
        enable_llm_classifier=_is_truthy(os.getenv("ENABLE_LLM_CLASSIFIER")),
        enable_llm_answer_generation=_is_truthy(
            os.getenv("ENABLE_LLM_ANSWER_GENERATION")
        ),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.6"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        cors_origins=_parse_csv(
            os.getenv(
                "CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173",
            )
        ),
    )


def _is_truthy(value: str | None) -> bool:
    if value is None:
        return False

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_csv(value: str | None) -> list[str]:
    if value is None:
        return []

    return [item.strip() for item in value.split(",") if item.strip()]
