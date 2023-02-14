from fastapi.testclient import TestClient
from main import app
import os
from dotenv import load_dotenv

load_dotenv()

def test_facebook_page():
    client = TestClient(app)
    response = client.get(f"/{os.getenv('PAGE_ID')}")
    assert response.status_code == 200
    assert "data" in response.json()
