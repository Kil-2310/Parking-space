import pytest
from tests.factories import ClientFactory, ParkingFactory, ClientParkingFactory


@pytest.mark.asyncio
async def test_create_client_with_factory(db_session):
    """Тест создания клиента через фабрику"""
    ClientFactory._meta.sqlalchemy_session = db_session
    client = ClientFactory()
    await db_session.commit()
    await db_session.refresh(client)

    assert client.client_id is not None
    assert client.name is not None
    assert client.surname is not None


@pytest.mark.asyncio
async def test_create_parking_with_factory(db_session):
    """Тест создания парковки через фабрику"""
    ParkingFactory._meta.sqlalchemy_session = db_session
    parking = ParkingFactory()
    await db_session.commit()
    await db_session.refresh(parking)

    assert parking.parking_id is not None
    assert parking.address is not None
    assert parking.count_places > 0