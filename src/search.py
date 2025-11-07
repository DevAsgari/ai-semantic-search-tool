import faiss
import numpy as np
from typing import List, Tuple


class SemanticSearch:
    def __init__(self, embeddings: np.ndarray, texts: List[str]) -> None:
        """
        Initialize semantic search with embeddings and texts.
        
        Args:
            embeddings: numpy array of embeddings (shape: n x dimension)
            texts: List of text strings corresponding to embeddings
        """
        self.texts: List[str] = texts
        self.dimension: int = embeddings.shape[1]
        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(self.dimension)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for most similar texts to the query embedding.
        
        Args:
            query_embedding: Query vector (shape: dimension,)
            top_k: Number of results to return
            
        Returns:
            List of tuples (text, similarity_score) sorted by similarity (highest first)
            Scores range from 0.0 to 1.0 (1.0 = highest similarity)
        """
        query = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query)
        distances, indices = self.index.search(query, top_k)
        results: List[Tuple[str, float]] = [
            (self.texts[i], float(distances[0][j])) for j, i in enumerate(indices[0])
        ]
        return results
