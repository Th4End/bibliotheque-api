import requests
import re
from os import getenv
from dotenv import load_dotenv

load_dotenv()
OpenLibrary_URL = getenv("OpenLibrary_URL")


def _extract_year(raw_date: str | None) -> int | None:
    if not raw_date:
        return None
    year_match = re.search(r"(\d{4})", raw_date)
    if not year_match:
        return None
    return int(year_match.group(1))


def fetch_openlibrary(isbn: str):
    url = f"{OpenLibrary_URL}/isbn/{isbn}.json"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None

    data = response.json()
    year = _extract_year(data.get("publish_date"))

    author_names = [
        author.get("name")
        for author in data.get("authors", [])
        if author.get("name")
    ]
    authors = ", ".join(author_names) if author_names else "Unknown"

    return {
        "title": data.get("title"),
        "authors": authors,
        "year": year,
    }
    