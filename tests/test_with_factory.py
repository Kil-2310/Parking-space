from tests.factories import ClientFactory, ParkingFactory

def test_create_client_with_factory(db_session):
    """Тест создания клиента через фабрику"""
    # Передаем сессию через Meta класс
    ClientFactory._meta.sqlalchemy_session = db_session
    client = ClientFactory()
    db_session.commit()
    
    assert client.client_id is not None
    assert client.name is not None
    assert client.surname is not None


def test_create_parking_with_factory(db_session):
    """Тест создания парковки через фабрику"""
    # Передаем сессию через Meta класс
    ParkingFactory._meta.sqlalchemy_session = db_session
    parking = ParkingFactory()
    db_session.commit()
    
    assert parking.parking_id is not None
    assert parking.address is not None
    assert parking.count_places > 0