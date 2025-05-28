import logging
from typing import Optional
from llm import get_llm_response, LLMError
from RAG.retrieval import retrieve_relevant_documents, get_document_stats
from data_processing.preprocess_docs import preprocess_document
from config import TOP_K_RESULTS

# Disable all external library logging, only show warnings, errors, and critical messages
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('ollama').setLevel(logging.WARNING)

# logging.getLogger("httpx").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.getLogger("ollama").setLevel(logging.WARNING)

def clear_screen():
    """Clear the terminal screen."""
    print("\033[H\033[J", end="")

# def clear_screen():
#     print("\033[H\033[J", end="")

def print_header():
    """Print the application header."""
    print("\n" + "="*50)
    print("LAWGPT".center(50))
    print("Your Legal Assistant".center(50))
    print("="*50 + "\n")
    print("Type 'quit' to exit or 'clear' to clear the screen.\n")


# def print_header():
#     print("\n" + "="*50)
#     print("LAWGPT".center(50))
#     print("Your Legal Assistant".center(50))
#     print("="*50 + "\n")
#     print("Type 'quit' to exit or 'clear' to clear the screen.\n")

def format_response(response: str, sources: list) -> str:
    """Format the response and sources in a clean way."""
    formatted = response.strip()
    if sources:
        formatted += "\n\n" + "─"*50 + "\n"
        formatted += "Sources:"
        for source in sources:
            formatted += f"\n• {source}"
    return formatted

# def format_response(response: str, sources: list) -> str:
#     formatted = response.strip()
#     if sources:
#         formatted += "\n\n" + "─"*50 + "\n"
#         formatted += "Sources:"
#         for source in sources:
#             formatted += f"\n• {source}"
#     return formatted

def process_query(user_query: str) -> Optional[str]:
    """
    Process a user query and return a response.
    
    Args:
        user_query (str): The user's question
    
    Returns:
        Optional[str]: The response, or None if processing failed
    """
    try:
        # Get document statistics
        stats = get_document_stats()
        
        if stats['total_documents'] == 0:
            return "I don't have any legal documents loaded yet. Please add some documents first."
        
        # Preprocess the query
        processed_query = preprocess_document(user_query)
        
        # Retrieve relevant documents
        relevant_docs = retrieve_relevant_documents(
            processed_query,
            top_k=TOP_K_RESULTS
        )
        
        # Extract document contents and metadata
        doc_contents = [doc['content'] for doc in relevant_docs] if relevant_docs else []
        doc_metadata = [doc['metadata'] for doc in relevant_docs] if relevant_docs else []
        
        # Get response from LLM
        response = get_llm_response(user_query, doc_contents)
        
        # Format sources if available
        if doc_metadata:
            sources = [
                f"{meta['filename']} (Last modified: {meta['last_modified']})"
                for meta in doc_metadata
            ]
            return format_response(response, sources)
        
        return response
        
    except LLMError:
        return "I'm having trouble processing your request right now. Please try again later."
    except Exception:
        return "An unexpected error occurred. Please try again later."


# def process_query(user_query: str) -> Optional[str]:
#     try:
#         stats = get_document_stats()
#         if stats['total_documents'] == 0:
#             return "I don't have any legal documents loaded yet. Please add some documents first."
#         processed_query = preprocess_document(user_query)
#         relevant_docs = retrieve_relevant_documents(processed_query)
#         doc_contents = [doc['content'] for doc in relevant_docs] if relevant_docs else []
#         doc_metadata = [doc['metadata'] for doc in relevant_docs] if relevant_docs else []
#         response = get_llm_response(user_query, doc_contents)
#         if doc_metadata:
#             sources = [
#                 f"{meta['filename']} (Last modified: {meta['last_modified']})"
#                 for meta in doc_metadata
#             ]
#             return format_response(response, sources)
#         return response
#     except LLMError:
#         return "I'm having trouble processing your request right now. Please try again later."
#     except Exception as e:
#         return f"An unexpected error {e} occurred. Please try again later."



def main():
    """Main application entry point."""
    clear_screen()
    print_header()
    
    while True:
        try:
            user_query = input("> ").strip()
            
            if user_query.lower() == 'quit':
                print("\nGoodbye!")
                break
                
            if user_query.lower() == 'clear':
                clear_screen()
                print_header()
                continue
                
            if not user_query:
                continue
                
            response = process_query(user_query)
            print("\n" + response + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception:
            print("\nAn error occurred. Please try again.")


def main():
    clear_screen()
    print_header()

    while True:
        try:
            user_query = input("> ").strip()
            
            if user_query.lower() == 'quit':
                print("\nGoodbye!")
                break
                
            if user_query.lower() == 'clear':
                clear_screen()
                print_header()
                continue
                
            if not user_query:
                continue
                
            response = process_query(user_query)
            print("\n" + response + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception:
            print("\nAn error occurred. Please try again.")



if __name__ == "__main__":
    main() 