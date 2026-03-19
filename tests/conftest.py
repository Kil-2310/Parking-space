import pytest
from fastapi.testclient import TestClient

from app import create_app
from database.models import Base
from database.database_models import Client, Parking

from database.models import sync_engine, sync_session

@pytest.fixture(autouse=True)
def setup_database():
    """Создает таблицы и тестовые данные для каждого теста"""
    Base.metadata.create_all(bind=sync_engine)
    
    with sync_session() as session:
        with session.begin():
            client_data = {
                "name": "Иван",
                "surname": "Петров",
                "credit_card": "1234-5678-9012-3456",
                "car_number": "А123БВ777"
            }
            db_client = Client(**client_data)
            session.add(db_client)

            parking_data = {
                "address": "ул. Ленина, д. 10",
                "opened": True,
                "count_places": 50,
                "count_available_places": 50
            }

            db_parking = Parking(**parking_data)
            session.add(db_parking)
    
    yield
    
    Base.metadata.drop_all(bind=sync_engine)


@pytest.fixture
def app():
    _app = create_app()
    _app.router.on_shutdown = []
    return _app


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    """Фикстура для работы с БД в тестах"""
    session = sync_session()
    try:
        yield session
    finally:
        session.close()