"""
FAISS Vector Store — Builds and queries the agricultural knowledge index.
Uses IndexFlatIP (Inner Product = cosine similarity on normalized vectors).
"""
import os
import json
import pickle
import numpy as np
import logging
from pathlib import Path
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

# Paths
KNOWLEDGE_PATH = Path(__file__).parent.parent / "knowledge" / "agri_knowledge.json"
INDEX_PATH = Path(__file__).parent.parent / "knowledge" / "faiss_index.bin"
DOCS_PATH = Path(__file__).parent.parent / "knowledge" / "docs_store.pkl"

# Singleton
_faiss_index = None
_documents: List[Dict] = []


def _load_documents() -> List[Dict]:
    """Load and prepare documents from the knowledge base JSON."""
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    docs = []
    for item in raw:
        # Create a combined text for embedding
        text = item.get("content", "")
        if item.get("crop"):
            text = f"Crop: {item['crop']}. {text}"
        if item.get("tags"):
            text = f"{text} Keywords: {', '.join(item['tags'])}"
        docs.append({
            "id": item.get("id", ""),
            "type": item.get("type", ""),
            "crop": item.get("crop", ""),
            "content": item.get("content", ""),
            "text": text,  # Text used for embedding
            "tags": item.get("tags", []),
        })
    return docs


def build_index(force_rebuild: bool = False):
    """Build FAISS index from knowledge base. Saves to disk for reuse."""
    global _faiss_index, _documents

    # Load from disk if already built
    if not force_rebuild and INDEX_PATH.exists() and DOCS_PATH.exists():
        logger.info("📂 Loading existing FAISS index from disk...")
        _documents = pickle.load(open(DOCS_PATH, "rb"))
        try:
            import faiss
            _faiss_index = faiss.read_index(str(INDEX_PATH))
            logger.info(f"✅ FAISS index loaded: {_faiss_index.ntotal} vectors")
            return
        except Exception as e:
            logger.warning(f"Failed to load index from disk: {e}. Rebuilding...")

    logger.info("⏳ Building FAISS index from knowledge base...")
    from app.ai.embeddings.embedder import embed_batch
    import faiss

    _documents = _load_documents()
    texts = [doc["text"] for doc in _documents]
    embeddings = embed_batch(texts)

    # Build IndexFlatIP (cosine similarity for normalized vectors)
    dim = embeddings.shape[1]  # 384
    _faiss_index = faiss.IndexFlatIP(dim)
    _faiss_index.add(embeddings)

    # Save to disk
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(_faiss_index, str(INDEX_PATH))
    pickle.dump(_documents, open(DOCS_PATH, "wb"))

    logger.info(f"✅ FAISS index built: {len(_documents)} documents, dim={dim}")


def retrieve(query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
    """
    Retrieve top-k most relevant documents for the query.
    Returns: List of (document, similarity_score) tuples.
    """
    global _faiss_index, _documents

    if _faiss_index is None or not _documents:
        logger.warning("FAISS index not initialized. Building now...")
        build_index()

    from app.ai.embeddings.embedder import embed_text

    query_vec = embed_text(query).reshape(1, -1)
    scores, indices = _faiss_index.search(query_vec, min(top_k, len(_documents)))

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx >= 0 and score > 0.1:  # Filter very low relevance
            results.append((_documents[idx], float(score)))

    logger.info(f"🔍 RAG: '{query[:50]}...' → {len(results)} docs retrieved, top score: {scores[0][0]:.3f}")
    return results


def get_context_string(query_or_results, max_chars: int = 3000) -> str:
    """Format retrieved documents into a context string for the LLM."""
    if isinstance(query_or_results, str):
        results = retrieve(query_or_results, top_k=3)
    else:
        results = query_or_results

    if not results:
        return "No relevant agricultural knowledge found for this query."

    context_parts = []
    total_chars = 0
    for item in results:
        if isinstance(item, tuple) and len(item) == 2:
            doc, score = item
        else:
            doc, score = item, 1.0
        text = f"[Source: {doc.get('type', 'kb')} | Relevance: {score:.2f}]\n{doc.get('content', '')}"
        if total_chars + len(text) > max_chars:
            break
        context_parts.append(text)
        total_chars += len(text)

    return "\n\n---\n\n".join(context_parts)
