from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_save_token():
    pass

def test_create_token():
    pass

def test_refresh_token():
    pass
