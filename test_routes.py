import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_calculate_total_cost():
    payload = {
        "currencies": ["USD", "EUR", "GBP"],
        "amounts": [100, 200, 150],
        "date": "2023-06-30"
    }

    response = client.post("/total_cost", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "total_cost" in data
    assert isinstance(data["total_cost"], float)


def test_get_exchange_rate():
    response = client.get("/exchange_rate?currency=USD&date=2023-06-30")
    assert response.status_code == 200
    assert response.json() == {
        "USD/PLN": 4.1325,
        "date": "2023-06-30"
    }


if __name__ == "__main__":
    pytest.main()
