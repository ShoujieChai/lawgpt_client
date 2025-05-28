import ollama
from typing import List
from config import LLM_MODEL, MAX_RETRIES, LLM_PROMPT_TEMPLATE

class LLMError(Exception):
    """Custom exception for LLM-related errors."""
    pass

# class LLMError(Exception):
#     pass

def get_llm_response(query: str, context: List[str], max_retries: int = MAX_RETRIES) -> str:
    """
    Get response from LLM with retry logic.
    
    Args:
        query (str): User's question
        context (List[str]): List of relevant document chunks
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        str: LLM's response
    
    Raises:
        LLMError: If all retry attempts fail
    """
    for attempt in range(max_retries):
        try:
            # If no context is provided, use a simpler prompt
            if not context:
                prompt = f"""You are a helpful legal assistant chatbot. While I don't have specific legal documents to reference for your question, I'll do my best to provide a general answer.

Question: {query}
Answer:"""
            else:
                # Format the prompt with context and query
                prompt = LLM_PROMPT_TEMPLATE.format(
                    context=' '.join(context),
                    query=query
                )
            
            # Get response from LLM
            response = ollama.chat(
                model=LLM_MODEL,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            return response['message']['content']
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise LLMError(f"Failed to get LLM response after {max_retries} attempts: {str(e)}") from e
            continue 


# def get_llm_response(query: str, context: List[str], max_retries: int = MAX_RETRIES):
#     for attempt in range(max_retries):
#         try: 
#             if not context: 
#                 promopt = f"""You are a helpful legal assistant chatbot. While I don't have specific legal documents to reference for your question, I'll do my best to provide a general answer.
#                      Question: {query}
#                     Answer:
#                 """
#             else:
#                 prompt = LLM_PROMPT_TEMPLATE.format(
#                     context=' '.join(context),
#                     query=query
#                 )
#             response = ollama.chat(
#                 model=LLM_MODEL,
#                 messages=[{'role': 'user', 'content': prompt}]
#             )
#             return response['message']['content']
#         except Exception as e:
#             if attempt == max_retries - 1:
#                 raise LLMError(f"Failed to get LLM response after {max_retries} attempts: {str(e)}") from e
#             continue