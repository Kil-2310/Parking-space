from pydantic import BaseModel
from datetime import datetime

# Пользователь

class BaseClient(BaseModel):
    name: str
    surname: str
    credit_card: str
    car_number: str


class BaseClientIn(BaseClient):
    ...


class BaseClientOut(BaseClient):
    client_id: int

    class Config:
        orm_mode = True

# Парковка

class BaseParking(BaseModel):
    address: str
    opened: bool
    count_places: int
    count_available_places: int

class BaseParkingIn(BaseParking):
    ...

class BaseParkingOut(BaseParking):
    parking_id: int

    class Config:
        orm_mode = True


# Заезд на парковку

class BaseClientParking(BaseModel):
    client_id: int
    parking_id: int


class BaseClientParkingIn(BaseClientParking):
    ...


class BaseClientParkingOut(BaseClientParking):
    client_parking_id: int
    time_in: datetime

    class Config:
        orm_mode = True


class BaseClientParkingDelete(BaseClientParking):
    client_parking_id: int
    time_out: datetime

    class Config:
        orm_mode = True

