import requests
import os

# Server endpoint and auth token
API_URL = "http://localhost:5001/query"
API_TOKEN = "secret-token-123"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# API_URL = "http;//localhost:500/query"
# API_TOKEN = "law_gpt_token"
# HEADERS = {
#     "Authorization": f"Bearer {API_TOKEN}",
#     "Content-Type": "application/json"
# }
# API_TOKEN = os.getenv("API_TOKEN", "default-token") # Use an environment variable for the API token
# def get_api_token():
#     """Prompt the user for the API token."""
#     return input("Enter your API token: ").strip()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("\n" + "="*50)
    print("LAWGPT CLIENT".center(50))
    print("Ask Legal Questions via API".center(50))
    print("="*50 + "\n")

def send_query_to_api(query: str) -> str:
    """Send query to the Flask API and return response string."""
    try:
        payload = {"query": query}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "(No response text)")
        else:
            return f"(Error {response.status_code}): {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"
    
# def send_query_to_api(query: str) -> str:
#     try:
#         payload = {"query": query}
#         response = requests.post(API_URL, headers=HEADERS, json=payload)
#         if response.status_code == 200:
#             return response.json().get("response", "(No response text)")
#         else: 
#             return f"(Error {response.status_code}): {response.text}"
#     except requests.exceptions.RequestException as e:
#         return f"An error occurred: {e}"

def main():
    """Main interactive CLI client."""
    clear_screen()
    print_header()
    print("Type 'quit' to exit or 'clear' to clear the screen.\n")

    while True:
        try:
            user_query = input("> ").strip()

            if user_query.lower() == 'quit':
                print("\nGoodbye!")
                break
            elif user_query.lower() == 'clear':
                clear_screen()
                print_header()
                continue
            elif not user_query:
                continue

            response_text = send_query_to_api(user_query)
            print("\n" + response_text + "\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")


# def main():
#     clear_screen()
#     print_header()
#     print("Type 'quit' to exit or 'clear' to clear the screen.\n")
#     while True:
#         try:
#             user_query = input("> "). strip()
#             if user_query.lower() == 'quit':
#                 print("\nGoodbye!")
#                 break
#             elif user_querr.lower() == 'clear':
#                 clear_screen()
#                 print_header()
#                 continue
#             elif not user_query:
#                 continue
#             response_text = send_query_to_api(user_query)
#             print(f"\n{response_text}\n")
#         except KeyboardInterrupt:
#             print("\nGoodbye!")
#             break
#         except Exception as e:
#             print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     main()
