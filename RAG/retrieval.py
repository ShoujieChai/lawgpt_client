import os
import json
import logging
from typing import List, Dict, Tuple
import numpy as np
from datetime import datetime
from RAG.embedding import get_embedding, compute_similarity
from config import (
    EMBEDDINGS_DIR,
    TOP_K_RESULTS,
    SIMILARITY_THRESHOLD
)  # () formats the imports across multiple lines

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger - logging.getLogger(__name__)


class DocumentMetadata:
    def __init__(self, filename: str, created_at: datetime, last_modified: datetime):
        self.filename = filename
        self.created_at = created_at
        self.last_modified = last_modified

# class DocumentMetadata:
#     def __init__(self, filename:str, created_at: datetime, last_modified: datetime):
#         self.filename = filename
#         self.created_at = created_at
#         self.last_modified = last_modified

def load_document_metadata(file_path: str) -> DocumentMetadata:
    """Load metadata for a document."""
    stats = os.stat(file_path)
    return DocumentMetadata(
        filename=os.path.basename(file_path),
        created_at=datetime.fromtimestamp(stats.st_ctime),
        last_modified=datetime.fromtimestamp(stats.st_mtime)
    )

# def load_document_metadata(file_path: str) -> DocumentMetadata:
#     stats = os.stat(file_path)
#     return DocumentMetadata(
#         filename = os.path.basename(file_path),
#         created_at = datetime.fromtimestamp(stats.st_ctime),
#         last_modified = datetime.fromtimestamp(stats.st_mtime)
#     )

def preprocess_query(query: str) -> str:
    """Preprocess the query to improve matching."""
    # Convert to lowercase
    query = query.lower()
    
    # Remove common words that might interfere with matching
    stop_words = {'what', 'when', 'where', 'who', 'why', 'how', 'is', 'are', 'was', 'were', 'the', 'a', 'an'}
    words = query.split()
    filtered_words = [w for w in words if w not in stop_words]
    
    return ' '.join(filtered_words)


# def preprocess_query(quer: str) -> str:
#     query = query.lower()
#     stop_words = {'what', 'when', 'where', 'who', 'why', 'how', 'is', 'are', 'was', 'were', 'the', 'a', 'an'}
#     words = query.split()
#     filtered_words = [w for w in words if w not in stop_words]
#     return ' '.join(filtered_words)


def retrieve_relevant_documents(
    query: str,
    top_k: int = TOP_K_RESULTS,
    min_similarity: float = SIMILARITY_THRESHOLD
) -> List[Dict]:
    """
    Retrieve the most relevant documents for a given query.
    
    Args:
        query (str): The search query
        top_k (int): Number of most relevant documents to return
        min_similarity (float): Minimum similarity threshold
    
    Returns:
        List[Dict]: List of relevant documents with their metadata and scores
    """
    if not os.path.exists(EMBEDDINGS_DIR):
        logger.warning(f"Embeddings directory {EMBEDDINGS_DIR} does not exist!")
        return []
    
    # Preprocess the query
    processed_query = preprocess_query(query)
    
    # Get query embedding
    query_embedding = get_embedding(processed_query)
    
    # Load and score documents
    scored_docs = []
    for filename in os.listdir(EMBEDDINGS_DIR):
        if not filename.endswith('.json'):
            continue
            
        file_path = os.path.join(EMBEDDINGS_DIR, filename)
        try:
            with open(file_path, 'r') as f:
                doc_data = json.load(f)
                
            doc_embedding = np.array(doc_data['embedding'])
            similarity = compute_similarity(query_embedding, doc_embedding)
            
            if similarity >= min_similarity:
                metadata = load_document_metadata(file_path)
                scored_docs.append({
                    'content': doc_data['content'],
                    'similarity': similarity,
                    'metadata': metadata.__dict__
                })
                
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")
            continue
    
    # Sort by similarity and get top k
    scored_docs.sort(key=lambda x: x['similarity'], reverse=True)
    return scored_docs[:top_k]


# def retrieve_relevant_embeddings(query: str, top_k: int = TOP_K_RESULTS, min_similarity = int =S SIMILARITY_THRESHOLD) -> List[Dict]:
#     if not os.path.exists(EMBEDDINGS_DIR):
#         logger.warning(f"Embeddding directory {EMBEDDINGS_DIR} does not exist!")
#         return []
#     processed_query = preprocess_query(query)
#     query_embedding = get_embedding(processed_query)
#     scored_docs = []
#     for filename in os.listdir(EMBEDDINGS_DIR):
#         if not filename.endswith('.json'):
#             continue
#         file_path = os.path.join(EMBEDDINGS_DIR, filename)
#         try:
#             with open(file_path, 'r') as f:
#                 doc_data = json.load(f)
#                 doc_embedding = np.array(doc_data['embedding'])
#                 similarity = compute_similarity(query_embedding, doc_embedding)
#             if similarity >= min_similarity:
#                     metadata = load_document_metadata(file_path)
#                     scored_docs.append({
#                         'content': doc_data['content'],
#                         'similarity': similarity,
#                         'metadata': metadata.__dict__
#                     })
#         except Exception as e:
#           logger.error(f"Error processing {filename}: {str(e)}")
#           continue
    
#     scored_docs.sort(key=lambda x: x['similarity'], reverse=True)
#     return scored_docs[:top_k]


def get_document_stats() -> Dict:
    """Get statistics about the document collection."""
    if not os.path.exists(EMBEDDINGS_DIR):
        return {
            'total_documents': 0,
            'total_chunks': 0,
            'average_chunks_per_doc': 0
        }
    
    doc_chunks = {}
    for filename in os.listdir(EMBEDDINGS_DIR):
        if filename.endswith('.json'):
            doc_name = filename.split('_chunk_')[0]
            doc_chunks[doc_name] = doc_chunks.get(doc_name, 0) + 1
    
    total_docs = len(doc_chunks)
    total_chunks = sum(doc_chunks.values())
    
    return {
        'total_documents': total_docs,
        'total_chunks': total_chunks,
        'average_chunks_per_doc': total_chunks / total_docs if total_docs > 0 else 0
    } 

# def get_document_stats() -> Dict:
#     if not os.path.exists(EMBEDDINGS_DIR):
#         return {
#             'total_documents': 0,
#             'total_chunks': 0,
#             'average_chunks_per_doc': 0
#         }
    
#     doc_chunks = {}
#     for filename in os.listdir(EMBEDDINGS_DIR):
#         if filename.endswith('.json'):
#             doc_name = filename.split('_chunk_')[0]
#             doc_chunks[doc_name] = doc_chunks.get(doc_name, 0) + 1
    
#     total_docs = len(doc_chunks)
#     total_chunks = sum(doc_chunks.values())
    
#     return {
#         'total_documents': total_docs,
#         'total_chunks': total_chunks,
#         'average_chunks_per_doc': total_chunks / total_docs if total_docs > 0 else 0
#     }
