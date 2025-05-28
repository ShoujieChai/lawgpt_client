import ollama
import numpy as np
from typing import Dict, Optional, List, Union
from functools import lru_cache
from config import EMBEDDING_MODEL

# import ollama
# import numpy as np
# from typing import Dict, Optional, List, Union
# from config import EMBEDDING_MODEL

class EmbeddingError(Exception):
    """Custom exception for embedding-related errors."""
    pass

# class EmbeddingError(Exception):
#     """Custom exception for unsupported embedding model errors."""
#     pass

def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
    """
    Normalize embedding vector to unit length.
    
    Args:
        embedding (np.ndarray): Input embedding vector
    
    Returns:
        np.ndarray: Normalized embedding vector
    """
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm

# def normalize_embedding(emberddding: np.ndarray) -> np.ndarray:
#     """
#     Normalize embedding vector to unit length.
    
#     Args:
#         embedding (np.ndarray): Input embedding vector
    
#     Returns:
#         np.ndarray: Normalized embedding vector
#     """
#     norm = np.linalg.norm(embedding)
#     if norm == 0:
#         return embedding
#     return embedding / norm

@lru_cache(maxsize=1000) # apply LRU cache to the get_embedding function
def get_embedding(text: str) -> np.ndarray:
    """
    Generate embeddings for a given text using the specified model.
    Results are cached to improve performance.
    
    Args:
        text (str): The text to generate embeddings for
    
    Returns:
        np.ndarray: The normalized embedding vector
    
    Raises:
        EmbeddingError: If the embedding generation fails
    """
    try:
        result = ollama.embeddings(
            model=EMBEDDING_MODEL,
            prompt=text
        )
        embedding = np.array(result['embedding'], dtype=np.float32)
        return normalize_embedding(embedding)
    except Exception as e:
        raise EmbeddingError(f"Failed to generate embedding: {str(e)}") from e


# def get_embedding(file_path: str) -> Optional[np.ndarray]:
#     try: 
#         result = ollama,embeddings (
#             model=EMBEDDING_MODEL,
#             prompt=file_path
#         )
#         embedding = np.array(result['embedding'], dtype=np.float32)
#         return normalize_embedding(embedding)
#     except Exception as e:
#         raise EmbeddingError(f"Failed to generate embedding: {str(e)}") from e

def compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Args:
        embedding1 (np.ndarray): First embedding vector
        embedding2 (np.ndarray): Second embedding vector
    
    Returns:
        float: Cosine similarity score between 0 and 1
    
    Raises:
        ValueError: If the embeddings have different dimensions
    """
    if embedding1.shape != embedding2.shape:
        raise ValueError(
            f"Embedding dimensions don't match: {embedding1.shape} vs {embedding2.shape}"
        )
    
    # Both vectors are already normalized, so dot product gives cosine similarity
    return float(np.dot(embedding1, embedding2))

# def compute_similarity_batch(embeddings1: np.ndarray, embeddings2: np.ndarray) -> float:
#     if embedding1.shape != embedding2.shape:
#         raise ValueError(
#             f"Embedding dimensions don't match: {embedding1.shape} vs {embedding2.shape}"
#         )
#     return float(np.dot(embedding1, embedding2))

def batch_get_embeddings(texts: List[str]) -> Dict[str, np.ndarray]:
    """
    Generate embeddings for multiple texts in batch.
    
    Args:
        texts (List[str]): List of texts to generate embeddings for
    
    Returns:
        Dict[str, np.ndarray]: Dictionary mapping texts to their normalized embeddings
    """
    embeddings = {}
    for text in texts:
        try:
            embeddings[text] = get_embedding(text)
        except EmbeddingError:
            continue
    return embeddings

# def batch_get_embeddings(texts: List[str]) -> Dict[str, np.ndarray]:
#     embeddings = {}
#     for text in texts:
#         try:
#             embeddings[test] = get_embedding(text)
#         except EmbeddingError:
#             continue
#     return embeddings

def get_embedding_stats(embedding: np.ndarray) -> Dict[str, float]:
    """
    Get statistics about an embedding vector.
    
    Args:
        embedding (np.ndarray): The embedding vector
    
    Returns:
        Dict[str, float]: Dictionary containing embedding statistics
    """
    return {
        'mean': float(np.mean(embedding)),
        'std': float(np.std(embedding)),
        'min': float(np.min(embedding)),
        'max': float(np.max(embedding)),
        'norm': float(np.linalg.norm(embedding))
    } 

# def get_embedding_stats(embedding: np.ndarray) -> Dict[str, float]:
#     return {
#         'mean': float(np.mean(embeddings)),
#         'std': float(np.std(embeddings)),
#         'min': float(np.min(embeddings)),
#         'max': float(np.max(embeddings)),
#         'norm': float(np.linalg.norm(embeddings))
#     }