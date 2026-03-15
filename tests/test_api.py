import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_process_video_endpoint():
    response = client.post("/process-video", json=[{"frame": 1}, {"frame": 2}])
    assert response.status_code == 200
    assert "video_path" in response.json()

@pytest.mark.asyncio
async def test_search_endpoint():
    response = client.post("/search", json={"query": "test"})
    assert response.status_code == 200
    assert "results" in response.json()
