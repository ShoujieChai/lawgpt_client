import requests

API_URL = "http://localhost:5000/query"
API_TOKEN = "secret-token-123"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def send_query_to_api(query: str) -> str:
    """Send query to the Flask API and return response string."""
    try:
        payload = {"query": query}
        print(f"Sending headers: {HEADERS}")  # Debugging
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        print(f"Response status code: {response.status_code}")  # Debugging
        print(f"Response text: {response.text}")  # Debugging
        if response.status_code == 200:
            return response.json().get("response", "(No response text)")
        elif response.status_code == 401:
            return "Error 401: Unauthorized. Check your API token."
        elif response.status_code == 403:
            return "Error 403: Forbidden. Check your API token or permissions."
        else:
            return f"(Error {response.status_code}): {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    query = "What is the legal definition of negligence?"
    print(send_query_to_api(query))