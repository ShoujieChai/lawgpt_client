# LLM Bootcamp LawGPT RAG Core Template

Welcome to the LawGPT RAG Template! This is a starter template for building a Retrieval-Augmented Generation (RAG) based legal assistant chatbot. This project will help you learn about RAG systems, document processing, and building AI-powered applications.

## Learning Objectives

By completing this project, you will learn:
- How to implement a RAG system from scratch
- Document processing and embedding generation
- Vector similarity search and retrieval
- Integration with local LLMs using Ollama
- Building a chatbot interface
- Best practices for handling legal documents

## Project Overview

This template provides an empty project structure that you'll need to implement. The goal is to create a legal assistant that:
- Processes and understands legal documents
- Retrieves relevant information based on user queries
- Generates accurate responses with source citations
- Runs entirely locally for privacy

## Project Structure

You'll need to implement the following files, please add if the files are not there :

```
lawgpt/
├── app.py                      # Main application file - implement the chatbot interface
├── llm.py                      # LLM interaction code - implement model calls
├── config.py                   # Configuration settings - define your parameters
├── data_processing/
│   ├── generate_embeddings.py  # Implement document embedding generation
│   └── preprocess_docs.py      # Implement document preprocessing
├── RAG/
│   ├── embedding.py           # Implement embedding functionality 
│   └── retrieval.py           # Implement vector retrieval functionality
├── data/
│   ├── documents/             # Place your legal documents here
│   └── embeddings/            # Generated embeddings will be stored here
└── requirements.txt           # Define your project dependencies
```

## Getting Started

### 1. Environment Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Create requirements.txt with necessary dependencies
# You'll need to add packages like:
# - langchain
# - chromadb
# - python-dotenv
# - fastapi
# - uvicorn
# - pypdf
# - python-docx
```

### 2. Install Ollama

#### macOS/Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows:
1. Download the installer from [Ollama's website](https://ollama.ai)
2. Run the installer and follow the instructions

### 3. Download Required Models

```bash
# Pull the LLM model for text generation
ollama pull mistral

# Pull the embedding model
ollama pull nomic-embed-text
```

## Implementation Guide

### 1. Document Processing
- Implement `preprocess_docs.py` to handle different document formats
- Create functions to extract text from PDFs, DOCX, and TXT files
- Implement text chunking and cleaning

### 2. Embedding Generation
- Implement `generate_embeddings.py` to create vector embeddings
- Use the nomic-embed-text model for generating embeddings
- Store embeddings in a vector database

### 3. RAG Implementation
- Implement retrieval logic in `retrieval.py`
- Create embedding functions in `embedding.py`
- Set up vector similarity search

### 4. LLM Integration
- Implement `llm.py` to handle interactions with the Mistral model
- Create prompt templates for legal queries
- Implement response generation with source citations

### 5. Application Interface
- Create a user interface in `app.py`
- Implement the main application logic
- Add error handling and logging

## Configuration

In `config.py`, you'll need to implement:
- `CHUNK_SIZE`: Size of document chunks for processing
- `TOP_K_RESULTS`: Number of relevant documents to retrieve
- `SIMILARITY_THRESHOLD`: Minimum similarity score for document matching
- Add any other configuration parameters you need

## Testing Your Implementation

1. Add sample legal documents to `data/documents/`
2. Run the preprocessing and embedding generation
3. Start the application and test with various legal queries
4. Verify that responses include proper source citations

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ollama](https://ollama.ai) for providing the LLM infrastructure
- [Nomic AI](https://nomic.ai) for the embedding model
