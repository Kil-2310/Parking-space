import pytest
import pytest_asyncio
import json
from datetime import datetime
from database.database_models import Client, Parking, ClientParking


def test_get_all_clints(client):
    response = client.get('/clients')

    assert response.status_code == 200


def test_get_clint_by_id(client):
    response = client.get('/clients/1')

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Иван'


def test_create_client(client):
    """Тест создания клиента"""
    client_data = {
        "name": "Иван",
        "surname": "Петров",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "А123БВ777"
    }
    
    response = client.put("/clients", json=client_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == client_data["name"]
    assert data["surname"] == client_data["surname"]


def test_create_parking(client):
    """Тест создания парковки"""
    parking_data = {
        "address": "ул. Ленина, д. 10",
        "opened": True,
        "count_places": 50,
        "count_available_places": 50
    }
    
    response = client.put("/parkings", json=parking_data)
    assert response.status_code == 201
    data = response.json()
    assert data["address"] == parking_data["address"]
    assert data["opened"] == parking_data["opened"]


@pytest.mark.car
def test_create_client_parking(client):
    """Тест въезда на парковку"""

    client_data = {
        "name": "Иван",
        "surname": "Петров",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "А123БВ777"
    }
    client_response = client.put("/clients", json=client_data)
    assert client_response.status_code == 201
    client_id = client_response.json()["client_id"]
    

    parking_data = {
        "address": "ул. Ленина, д. 10",
        "opened": True,
        "count_places": 50,
        "count_available_places": 50
    }
    parking_response = client.put("/parkings", json=parking_data)
    assert parking_response.status_code == 201
    parking_id = parking_response.json()["parking_id"]
    
    # Въезд
    client_parking_data = {
        "client_id": client_id,
        "parking_id": parking_id
    }
    
    response = client.put("/client_parkings", json=client_parking_data)
    assert response.status_code == 201
    data = response.json()
    assert "client_parking_id" in data

@pytest.mark.car
def test_delete_client_parking(client):
    """Тест выезда с парковки"""
    # Создаем клиента
    client_data = {
        "name": "Иван",
        "surname": "Петров",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "А123БВ777"
    }
    client_response = client.put("/clients", json=client_data)
    assert client_response.status_code == 201
    client_id = client_response.json()["client_id"]

    # Создаем парковку
    parking_data = {
        "address": "ул. Ленина, д. 10",
        "opened": True,
        "count_places": 50,
        "count_available_places": 50
    }
    parking_response = client.put("/parkings", json=parking_data)
    assert parking_response.status_code == 201
    parking_id = parking_response.json()["parking_id"]

    # Въезд
    client_parking_data = {
        "client_id": client_id,
        "parking_id": parking_id
    }
    create_response = client.put("/client_parkings", json=client_parking_data)
    assert create_response.status_code == 201

    response = client.request(
        method="DELETE",
        url="/client_parkings",
        json=client_parking_data
    )
    assert response.status_code == 200

@pytest.mark.parametrize("resp", ['/clients', '/clients/1'])
def test_all_get_response(client, resp):
    response = client.get(resp)

    assert response.status_code == 200