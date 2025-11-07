from sentence_transformers import SentenceTransformer
from typing import Union, List
import numpy as np


class Embedder:
    def __init__(self, model: str = "sentence-transformers/all-mpnet-base-v2") -> None:
        """
        Initialize the embedder with a Sentence-BERT model.
        
        Args:
            model: Model name or path for SentenceTransformer
        """
        self.model = SentenceTransformer(model)

    def __call__(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encode text(s) into embeddings.
        
        Args:
            texts: Single string or list of strings to embed
            
        Returns:
            numpy array of embeddings
            - Shape (768,) for single string input
            - Shape (n, 768) for list of n strings
        """
        return self.model.encode(texts)
