# import os
# import json
# import re
# from nltk.corpus import stopwords
# from PyPDF2 import PdfReader
# from docx import Document

import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from typing import List, Dict, Any

def download_nltk_data():
    """Download required NLTK data."""
    required_packages = [
        'punkt',
        'stopwords',
        'punkt_tab'
    ]
    
    for package in required_packages:
        try:
            if package == 'punkt_tab':
                nltk.download('punkt_tab', quiet=True)
            else:
                nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            print(f"Downloading NLTK {package} data...")
            nltk.download(package, quiet=True)
            print(f"Downloaded NLTK {package} data.")


# Download required NLTK data at module import
download_nltk_data()


# def clean_text(text: str) -> str:
#     # Remove special characters and punctuation
#     text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
#     # Remove extra spaces
#     text = re.sub(r"\s+", " ", text).strip()
#     return text

def clean_text(text: str) -> str:
    """
    Clean and normalize text while preserving important structure.
    
    Args:
        text (str): The input text to clean
    
    Returns:
        str: Cleaned text
    """
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Preserve numbers and important punctuation
    text = re.sub(r'[^\w\s\d\-\.]', ' ', text)
    
    # Remove extra whitespace
    text = text.strip()
    
    return text


# def extract_numbers(text: str) -> list[str]:
#     # Find all sequences of digits in the text
#     numbers = re.findall(r"\d+", text)
#     return numbers


def extract_numbers(text: str) -> List[str]:
    """
    Extract numbers and numerical patterns from text.
    
    Args:
        text (str): Input text
    
    Returns:
        List[str]: List of extracted numbers and numerical patterns
    """
    # Match various number patterns
    patterns = [
        r'\d+',  # Simple numbers
        r'\d+\.\d+',  # Decimal numbers
        r'\d+%',  # Percentages
        r'\$\d+(?:\.\d+)?',  # Currency
        r'\d+(?:st|nd|rd|th)',  # Ordinal numbers
    ]
    
    numbers = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        numbers.extend(match.group() for match in matches)
    
    return numbers


# def preprocess_text(text: str) -> str:
#     text = clean_text(text)
#     numbers = extract_numbers(text)
#     text = text.lower()
#     words = text.split()
#     stop_words = set(stopwords.words('english'))
#     """
#     Keep words that are: 
#     1. Not in stopwords
#     2. Not digits
#     3. Not a combination of letters and digits
#     """
#     filtered_words = []
#     for word in words:
#         if (word not in stop_words or
#             word.isdigit() or
#             re.match(r'^[a-z]+\d+$', word) or
#             re.match(r'^[a-z]+-[a-z]+$', word)):
#             filtered_words.append(word)

#     filtered_words.extend(numbers)
#     return ' '.join(filtered_words)

def preprocess_document(text: str) -> str:
    """
    Preprocess a document by cleaning and normalizing the text.
    
    Args:
        text (str): The input text to preprocess
    
    Returns:
        str: Preprocessed text
    """
    # Clean the text first
    text = clean_text(text)
    
    # Extract numbers before converting to lowercase
    numbers = extract_numbers(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove stopwords but preserve numbers and important terms
    stop_words = set(stopwords.words('english'))
    words = text.split()
    
    # Keep words that are:
    # 1. Not in stopwords
    # 2. Numbers
    # 3. Important terms (like h-1b, lca, etc.)
    filtered_words = []
    for word in words:
        if (word not in stop_words or
            word.isdigit() or
            re.match(r'^[a-z]+\d+$', word) or  # Matches patterns like "h1b"
            re.match(r'^[a-z]+-[a-z]+$', word)):  # Matches patterns like "h-1b"
            filtered_words.append(word)
    
    # Add extracted numbers back
    filtered_words.extend(numbers)
    
    return ' '.join(filtered_words)

# def split_into_chunks(text: str, chunk_size: int) -> list[str]:
#     """
#     Splits the input text into chunks of the specified size.

#     Args:
#         text (str): The input text to be split.
#         chunk_size (int): The size of each chunk.

#     Returns:
#         list[str]: A list of text chunks.
#     """
#     if not text:
#         return []

#     # Split the text into chunks of size `chunk_size`
#     chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
#     return chunks

def split_into_chunks(text: str, chunk_size: int = 1000) -> List[str]:
    """
    Split text into smaller chunks for processing.
    
    Args:
        text (str): The input text
        chunk_size (int): Maximum size of each chunk
    
    Returns:
        List[str]: List of text chunks
    """
    try:
        # First try to split by newlines to preserve structure
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        # If paragraphs are too long, try sentence tokenization
        if any(len(p.split()) > chunk_size for p in paragraphs):
            try:
                sentences = sent_tokenize(text)
            except LookupError as e:
                print(f"Error with NLTK data: {str(e)}")
                print("Attempting to download required NLTK data...")
                download_nltk_data()
                try:
                    sentences = sent_tokenize(text)
                except LookupError as e:
                    print(f"Failed to download NLTK data: {str(e)}")
                    sentences = [s.strip() for s in text.split('.') if s.strip()]
        else:
            sentences = paragraphs
    except Exception as e:
        print(f"Error in text splitting: {str(e)}")
        sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence_size = len(sentence.split())
        if current_size + sentence_size > chunk_size:  # if the current chunk is full that can not add another new senstence, add it to the list of chunks
            if current_chunk:  # Only add if we have content
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]   
            current_size = sentence_size
        else:  # if the current chunk still have space to add the sentence,  add the sentence to the current chunk
            current_chunk.append(sentence)
            current_size += sentence_size  # add the size of the sentence to the current chunk size
    
    if current_chunk:  # for any remaining sentences that does not fill a chunk annd will be added to the last chunk
        chunks.append(' '.join(current_chunk))
    
    return chunks 