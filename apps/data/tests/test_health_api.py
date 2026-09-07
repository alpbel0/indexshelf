from fastapi.testclient import TestClient

from indexshelf_data.apps.health_api import app


def test_live_health_endpoint_reports_live() -> None:
    response = TestClient(app).get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "live"}
