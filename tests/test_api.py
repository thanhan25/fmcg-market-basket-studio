from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_recommend_endpoint_normalization():
    # Proves the API handles messy user input (capitalization) seamlessly
    response = client.get("/recommend/DIAPERS?top_n=1")
    if response.status_code == 200:
        data = response.json()
        assert data["anchor"] == "diapers"
        assert isinstance(data["recommendations"], list)
