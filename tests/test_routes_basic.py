from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_books_unauth():
    response = client.get("/books/")
    assert response.status_code in (401, 403)

def test_get_tags():
    response = client.get("/tags/")
    assert response.status_code in (200, 401, 403)

def test_search_books():
    response = client.get("/search/search?q=test")
    assert response.status_code in (200, 401, 403)
