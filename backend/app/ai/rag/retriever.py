"""
RAG Retriever — High-level interface combining embedder + FAISS store.
"""
import logging
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)


async def retrieve_context(
    query: str,
    crop: Optional[str] = None,
    top_k: int = 5,
) -> Tuple[str, List[Dict]]:
    """
    Retrieve relevant documents for a query.
    Returns: (context_string, list_of_doc_metadata)
    """
    from app.ai.vector_store.faiss_store import retrieve, get_context_string

    # Enrich query with crop name for better retrieval
    search_query = f"{crop} {query}" if crop and crop != "General" else query

    results = retrieve(search_query, top_k=top_k)
    context = get_context_string(results)
    doc_metadata = [
        {
            "content_preview": doc["content"][:150] + "...",
            "type": doc["type"],
            "crop": doc.get("crop", ""),
            "relevance_score": round(score, 3),
        }
        for doc, score in results
    ]

    logger.info(f"🔍 Retrieved {len(results)} docs for query: '{query[:40]}'")
    return context, doc_metadata
