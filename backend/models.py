from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(11, 8), nullable=False)

class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bike_id = Column(String(50), nullable=False)
    start_station_id = Column(String(50), nullable=False)
    end_station_id = Column(String(50), nullable=False)
    started_at = Column(TIMESTAMP, nullable=False)
    ended_at = Column(TIMESTAMP, nullable=False) 