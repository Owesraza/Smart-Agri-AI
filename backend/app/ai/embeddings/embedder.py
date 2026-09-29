"""
Sentence Transformer Embedder
Model: all-MiniLM-L6-v2 (384 dimensions, fast, multilingual capable)
"""
import numpy as np
import logging
from typing import List, Union
from functools import lru_cache

logger = logging.getLogger(__name__)

# Lazy-loaded model singleton
_model = None


def get_embedder():
    """Return singleton SentenceTransformer model (loaded once)."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("⏳ Loading SentenceTransformer model: all-MiniLM-L6-v2...")
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("✅ Embedding model loaded successfully")
        except ImportError:
            logger.error("sentence-transformers not installed. Run: pip install sentence-transformers")
            raise
    return _model


def embed_text(text: str) -> np.ndarray:
    """Embed a single text string → numpy array (384,)."""
    model = get_embedder()
    embedding = model.encode(text, normalize_embeddings=True)
    return np.array(embedding, dtype=np.float32)


def embed_batch(texts: List[str], batch_size: int = 32) -> np.ndarray:
    """Embed a list of texts → numpy array (N, 384)."""
    model = get_embedder()
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=len(texts) > 50,
    )
    return np.array(embeddings, dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two normalized vectors."""
    return float(np.dot(a, b))
