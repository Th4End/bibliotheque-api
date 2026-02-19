import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
OpenLibrary_URL = getenv("OpenLibrary_URL")
def fetch_openlibrary(isbn: str):
    url = f"{OpenLibrary_URL}/isbn/{isbn}.json"
    response = requests.get(url)
    if response.status_code != 200:
        return None
        
    data = response.json()

    year = data.get("publish_date")
    if year:
        year = int(year.split()[-1])
        return{
            "title": data.get("title"),
            "authors": [author.get("name") for author in data.get("authors", [])],
            "year": year if year else None,
        }
    