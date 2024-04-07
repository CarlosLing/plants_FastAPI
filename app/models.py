from sqlalchemy import Column, Float, String, DateTime, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


# Define your models, e.g., Sensor and SensorReading
class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    measurement = Column(String)
    name = Column(String, unique=True)
    description = Column(String)

    readings = relationship("SensorReading", back_populates="sensor")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))

    sensor = relationship("Sensor", back_populates="readings")
