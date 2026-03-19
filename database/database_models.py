from .models import Base
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, \
    DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime


class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    surname = Column(VARCHAR(50), nullable=False)
    credit_card = Column(VARCHAR(50), nullable=False)
    car_number = Column(VARCHAR(10), nullable=False)

    client_parking = relationship('ClientParking', back_populates='client')

class Parking(Base):
    __tablename__ = 'parking'

    parking_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(VARCHAR(100), nullable=False)
    opened = Column(Boolean, default=True)
    count_places = Column(Integer, nullable=False)
    count_available_places = Column(Integer, nullable=False)

    client_parking = relationship('ClientParking', back_populates='parking')


class ClientParking(Base):
    __tablename__ = 'client_parking' 

    __table_args__ = (
        UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

    client_parking_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(ForeignKey('client.client_id'))
    parking_id = Column(ForeignKey('parking.parking_id'))
    time_in = Column(DateTime, default=datetime.now)
    time_out = Column(DateTime)

    client = relationship('Client', back_populates='client_parking')
    parking = relationship('Parking', back_populates='client_parking')
