import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parents[2] / "knowledge_base"
POLICY_FILES = {
    "return_policy": "return_policy.txt",
    "shipping_policy": "shipping_policy.txt",
    "warranty_policy": "warranty_policy.txt",
}
STOP_WORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "can",
    "does",
    "for",
    "from",
    "how",
    "into",
    "the",
    "this",
    "that",
    "what",
    "when",
    "where",
    "with",
    "within",
    "your",
}


@dataclass(frozen=True)
class PolicyChunk:
    policy: str
    source: str
    chunk_id: str
    text: str
    term_counts: Counter[str]


def search_policy(
    query: str,
    policy_type: str | None = None,
    limit: int = 3,
) -> list[dict[str, str | float]]:
    chunks = _load_policy_chunks(policy_type)
    if not chunks:
        return []

    query_vector = _build_query_vector(query, chunks)
    if not query_vector:
        return []

    scored_chunks = [
        (_cosine_similarity(query_vector, _build_chunk_vector(chunk, chunks)), chunk)
        for chunk in chunks
    ]

    results = [
        _format_result(chunk, score)
        for score, chunk in sorted(scored_chunks, key=lambda item: item[0], reverse=True)
        if score > 0
    ]
    return results[:limit]


def _load_policy_chunks(policy_type: str | None = None) -> list[PolicyChunk]:
    chunks: list[PolicyChunk] = []

    for policy_name, file_name in POLICY_FILES.items():
        if policy_type and not policy_name.startswith(policy_type):
            continue

        file_path = KNOWLEDGE_BASE_DIR / file_name
        content = file_path.read_text(encoding="utf-8")

        for index, text in enumerate(_split_policy(content)):
            chunks.append(
                PolicyChunk(
                    policy=policy_name,
                    source=file_name,
                    chunk_id=f"{policy_name}:{index}",
                    text=text,
                    term_counts=Counter(_tokenize(text)),
                )
            )

    return chunks


def _split_policy(content: str) -> list[str]:
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return [chunk for chunk in chunks if not chunk.lower().endswith("policy")]


def _tokenize(text: str) -> list[str]:
    cleaned = "".join(character.lower() if character.isalnum() else " " for character in text)
    return [
        word
        for word in cleaned.split()
        if len(word) > 2 and word not in STOP_WORDS
    ]


def _build_query_vector(query: str, chunks: list[PolicyChunk]) -> dict[str, float]:
    return _build_tfidf_vector(Counter(_tokenize(query)), chunks)


def _build_chunk_vector(chunk: PolicyChunk, chunks: list[PolicyChunk]) -> dict[str, float]:
    return _build_tfidf_vector(chunk.term_counts, chunks)


def _build_tfidf_vector(
    term_counts: Counter[str],
    chunks: list[PolicyChunk],
) -> dict[str, float]:
    total_documents = len(chunks)
    vector: dict[str, float] = {}

    for term, count in term_counts.items():
        document_frequency = sum(1 for chunk in chunks if term in chunk.term_counts)
        inverse_document_frequency = math.log((1 + total_documents) / (1 + document_frequency)) + 1
        vector[term] = count * inverse_document_frequency

    return vector


def _cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    shared_terms = set(left).intersection(right)
    numerator = sum(left[term] * right[term] for term in shared_terms)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0 or right_norm == 0:
        return 0

    return numerator / (left_norm * right_norm)


def _format_result(chunk: PolicyChunk, score: float) -> dict[str, str | float]:
    return {
        "policy": chunk.policy,
        "source": chunk.source,
        "chunk_id": chunk.chunk_id,
        "score": round(score, 4),
        "text": chunk.text,
    }
