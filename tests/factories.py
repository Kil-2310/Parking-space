import random
from datetime import datetime

import factory
import factory.fuzzy as fuzzy

from database.database_models import Client, ClientParking, Parking
from database.models import sync_session


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = sync_session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.Faker("credit_card_number", card_type="visa")
    car_number = factory.LazyAttribute(
        lambda x: f"{random.choice(['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х'])}{random.randint(1, 9)} \
        {random.randint(0, 9)}{random.randint(0, 9)}\
        {random.choice(['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х'])}\
        {random.randint(1, 9)}{random.randint(0, 9)}"
    )


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = sync_session

    address = factory.Faker("address")
    opened = factory.Faker("boolean", chance_of_getting_true=80)
    count_places = fuzzy.FuzzyInteger(10, 500)
    count_available_places = factory.LazyAttribute(
        lambda obj: random.randint(0, obj.count_places)
    )


class ClientParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ClientParking
        sqlalchemy_session = sync_session

    client = factory.SubFactory(ClientFactory)
    parking = factory.SubFactory(ParkingFactory)
    time_in = factory.LazyFunction(datetime.now)
    time_out = factory.LazyAttribute(
        lambda obj: datetime.now() if random.choice([True, False]) else None
    )
