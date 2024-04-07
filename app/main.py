from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/sensors/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    db_user = crud.get_sensor_name(db, name=sensor.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name of sensor already exists")
    return crud.create_sensor(db=db, sensor=sensor)


@app.get("/sensors/", response_model=list[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud.get_sensors(db, skip=skip, limit=limit)
    return sensors


@app.put("/sensors/{sensor_id}")
async def update_sensor(
    sensor_id: str, sensor: schemas.SensorUpdate, db: Session = Depends(get_db)
):
    db_sensor = crud.update_sensor(db, sensor_id, sensor)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_sensor


@app.delete("/sensors/{sensor_id}")
async def delete_sensor(sensor_id: str, db: Session = Depends(get_db)):
    success = crud.delete_sensor(db, sensor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor not found")
    else:
        return {"message": "Item deleted successfully"}


# Define other endpoints as needed

# @app.get("/sensors/")
# async def get_sensors(db: Session = Depends(get_db)):
#     return db.query(models.Sensor).all()

# @app.get("/sensors/")
# async def get_sensors(id: Optional[str] = None, **filters):
#     print(id)
#     if id:
#         return sensors.get(id, {})
#     if filters:
#         return {sensor_id: sensor for sensor_id, sensor in sensors.items() if all(getattr(sensor, k, None) == v for k, v in filters.items())}
#     return list(sensors.values())

# @app.post("/sensors/")
# async def create_sensor(sensor: models.Sensor, db: Session = Depends(get_db)):
#     db.add(sensor)
#     db.commit()
#     db.refresh(sensor)
#     return sensor

# @app.get("/sensor_readings/")
# async def get_sensor_readings(sensor_id: str, n_samples: Optional[int] = None, n_days: Optional[int] = None):
#     readings = sensor_readings.get(sensor_id, [])
#     if n_samples:
#         return readings[-n_samples:]
#     if n_days:
#         cutoff = datetime.now() - timedelta(days=n_days)
#         return [reading for reading in readings if reading['timestamp'] > cutoff]
#     return readings

# @app.post("/sensor_readings/")
# async def add_sensor_reading(reading: SensorReading):
#     if reading.sensor_id not in sensors:
#         raise HTTPException(status_code=404, detail="Sensor not found")
#     if reading.sensor_id not in sensor_readings:
#         sensor_readings[reading.sensor_id] = []
#     sensor_readings[reading.sensor_id].append(reading.dict())
#     return {"message": "Reading added"}
