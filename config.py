import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "data")
# DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
# EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")

# Model settings
LLM_MODEL = "llama3.2"
# LLM_MODEL = "mistral"
EMBEDDING_MODEL = "nomic-embed-text"

# RAG settings
CHUNK_SIZE = 500  # Reduced chunk size for more granular retrieval
TOP_K_RESULTS = 5  # Increased number of results
SIMILARITY_THRESHOLD = 0.5  # Lowered threshold to get more matches
MAX_RETRIES = 3

# LLM Prompt Template
LLM_PROMPT_TEMPLATE = """You are a legal assistant chatbot. Your task is to answer questions based on the provided context.

Context information is below:
---------------------
{context}
---------------------

Given the context information, please follow these guidelines:
1. If the context contains relevant information, provide a clear and concise answer
2. If the context doesn't contain relevant information, provide a general answer but clearly state that this information is not available in the provided documents
3. Always maintain a professional and helpful tone
4. If you're unsure about something, say so

Question: {query}
Answer:"""

# System prompts 
LEGAL_ASSISTANT_PROMPT = """
You are a legal assistant chatbot. Use the provided context to answer legal questions accurately.
If you're unsure about something, say so. Always cite your sources when possible.
Follow these guidelines:
1. Provide clear, concise answers
2. Cite relevant laws or regulations when possible
3. Explain complex legal terms in simple language
4. If the context doesn't contain relevant information, say so
5. Always maintain a professional tone
"""

# File extensions
SUPPORTED_DOCUMENT_TYPES = ('.txt', '.pdf', '.doc', '.docx')

# Create necessary directories
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True) 