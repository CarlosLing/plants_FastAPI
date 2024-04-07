from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SensorBase(BaseModel):
    location: str
    measurement: str
    name: str
    description: Optional[str] = None


class SensorCreate(SensorBase):
    pass


class SensorUpdate(SensorBase):
    location: Optional[str] = None
    measurement: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class SensorReadingBase(BaseModel):
    value: float
    timestamp: datetime = datetime.now()


class SensorReadingCreate(SensorReadingBase):
    pass


class SensorReading(SensorReadingBase):
    id: int
    sensor_id: int

    class Config:
        orm_mode = True


class Sensor(SensorBase):
    id: int
    readings: List[SensorReading] = []

    class Config:
        orm_mode = True
