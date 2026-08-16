import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    enable_llm_classifier: bool
    openai_api_key: str | None
    openai_model: str
    openai_base_url: str


def get_settings() -> Settings:
    return Settings(
        enable_llm_classifier=_is_truthy(os.getenv("ENABLE_LLM_CLASSIFIER")),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.6"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def _is_truthy(value: str | None) -> bool:
    if value is None:
        return False

    return value.strip().lower() in {"1", "true", "yes", "on"}
