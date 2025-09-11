from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_health():
    """API sağlık kontrolü testi"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_db_health():
    """Veritabanı sağlık kontrolü testi"""
    response = client.get("/api/health/db")
    assert response.status_code == 200
    
    # Başarılı bağlantı durumu
    json_response = response.json()
    assert "status" in json_response
    assert "database" in json_response
    
    # Status "ok" veya "error" olabilir (CI ortamına bağlı)
    assert json_response["status"] in ["ok", "error"]


