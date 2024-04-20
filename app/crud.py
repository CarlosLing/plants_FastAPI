from sqlalchemy.orm import Session
from . import schemas
from .models import Sensor, SensorReading
from pdb import set_trace
from sqlalchemy import desc


def get_sensor(db: Session, sensor_id: int):
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def get_sensor_readings(db: Session, sensor_id: int, limit: int = None):
    query = (
        db.query(SensorReading)
        .filter(SensorReading.sensor_id == sensor_id)
        .limit(limit)
    )
    values = [e.value for e in query]
    timestamps = [e.timestamp for e in query]
    return {"values": values, "timestamps": timestamps}


def get_latest_reading(db: Session, sensor_id: int):
    reading = (
        db.query(SensorReading)
        .filter(SensorReading.sensor_id == sensor_id)
        .order_by(desc(SensorReading.timestamp))
        .first()
    )
    return reading


def get_sensor_name(db: Session, name: str):
    return db.query(Sensor).filter(Sensor.name == name).first()


def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sensor).offset(skip).limit(limit).all()


def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = Sensor(
        location=sensor.location,
        measurement=sensor.measurement,
        name=sensor.name,
        description=sensor.description,
    )
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def update_sensor(
    db: Session, sensor_id: int, item_update: schemas.SensorUpdate
) -> Sensor:
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if db_sensor is None:
        return None
    for var, value in vars(item_update).items():
        setattr(db_sensor, var, value) if value else None
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def delete_sensor(db: Session, sensor_id: int) -> bool:
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if db_sensor is None:
        return False
    db.delete(db_sensor)
    db.commit()
    return True


def create_sensor_reading(db: Session, sensor_id: schemas.SensorCreate, value: float):
    new_reading = SensorReading(value=value, sensor_id=sensor_id)
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return new_reading
