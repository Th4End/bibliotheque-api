import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
GoogleBooks_URL = getenv("GoogleBooks_URL")

def fetch_from_googlebook(isbn: str):
    url = f"{GoogleBooks_URL}{isbn}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
        
    data = response.json()
    if "items" not in data or len(data["items"]) == 0:
        return None

    book_info = data["items"][0]["volumeInfo"]
    return {
        "title": book_info.get("title"),
        "authors": ", ".join(book_info.get("authors", [])),
        "year": book_info.get("publishedDate", "")[:4]
    }