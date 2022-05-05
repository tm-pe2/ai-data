#!/usr/bin/env python3

from typing import Any

from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, Integer, Sequence, Float
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    occupants = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    solar_panels = Column(Boolean)
    isolated = Column(Boolean)

    def __init__(
            self,
            occupants: int,
            latitude: float,
            longitude: float,
            solar_panels: bool,
            isolated: bool,
            *args: Any,
            **kwargs: Any
            ) -> None:
        super().__init__(*args, **kwargs)

        self.occupants = occupants
        self.latitude = latitude
        self.longitude = longitude
        self.solar_panels = solar_panels
        self.isolated = isolated

    def __str__(self):
        return f"occupants: {self.occupants}, latitude: {self.latitude}, \
longitude: {self.longitude}, solar_panels: {self.solar_panels}, \
isolated: {self.isolated}"


def get_db_connection(ip: str, username: str, password: str, db: str) -> Engine:
    engine = create_engine(f"postgresql+pg8000://{username}:{password}@{ip}:5432/{db}")
    Base.metadata.create_all(engine)

    return engine

if __name__ == "__main__":
    # Setup
    engine = get_db_connection('localhost', 'postgres', 'toor123', 'postgres')
    Session = sessionmaker(engine)  
    with Session() as session:
        # Create
        customer1 = Customer(-1337, 1337, 1337, True, False)
        customer2 = Customer(occupants=-1337, latitude=2, longitude=3,
                solar_panels=True, isolated=False)
        session.add(customer1)
        session.add(customer2)
        session.commit()

        # Read
        customers = session.query(Customer)
        print("=" * 20)
        for customer in customers:
            print(customer)

        print("=" * 20)
        customer = session.query(Customer).filter(
                Customer.occupants >= 2,
                Customer.isolated == False,
                )

        for customer in customers:
            print(customer)

        # Update
        customer1.latitude = -1337
        session.commit()

    session = Session()
    # Delete
    session.query(Customer).filter(
            Customer.occupants == -1337,
            ).delete()

    session.commit()
    session.close()
