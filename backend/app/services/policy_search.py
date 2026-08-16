from pathlib import Path


KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parents[2] / "knowledge_base"
POLICY_FILES = {
    "return_policy": "return_policy.txt",
    "shipping_policy": "shipping_policy.txt",
    "warranty_policy": "warranty_policy.txt",
}


def search_policy(query: str, policy_type: str | None = None) -> list[dict[str, str | int]]:
    query_terms = _tokenize(query)
    results: list[dict[str, str | int]] = []

    for policy_name, file_name in POLICY_FILES.items():
        if policy_type and not policy_name.startswith(policy_type):
            continue

        file_path = KNOWLEDGE_BASE_DIR / file_name
        content = file_path.read_text(encoding="utf-8")

        for chunk_index, chunk in enumerate(_split_policy(content)):
            score = _score_chunk(query_terms, chunk)
            if score > 0:
                results.append(
                    {
                        "policy": policy_name,
                        "chunk_index": chunk_index,
                        "score": score,
                        "text": chunk,
                    }
                )

    return sorted(results, key=lambda result: result["score"], reverse=True)[:3]


def _split_policy(content: str) -> list[str]:
    return [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]


def _tokenize(text: str) -> set[str]:
    cleaned = "".join(character.lower() if character.isalnum() else " " for character in text)
    return {word for word in cleaned.split() if len(word) > 2}


def _score_chunk(query_terms: set[str], chunk: str) -> int:
    chunk_terms = _tokenize(chunk)
    return len(query_terms.intersection(chunk_terms))
