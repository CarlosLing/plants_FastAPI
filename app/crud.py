from sqlalchemy.orm import Session
from . import models, schemas


def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def get_sensor_name(db: Session, name: str):
    return db.query(models.Sensor).filter(models.Sensor.name == name).first()


def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()


def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(
        location=sensor.location,
        measurement=sensor.measurement,
        name=sensor.name,
        description=sensor.description,
    )
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


# Implement other CRUD operations as needed
