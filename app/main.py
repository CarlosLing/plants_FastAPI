from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/sensors/{sensor_id}", response_model=schemas.Sensor)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


@app.get("/sensors/{sensor_id}/readings", response_model=schemas.SensorReadingArray)
def get_sensor_readings(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    readings = crud.get_sensor_readings(db=db, sensor_id=sensor_id)
    return readings


@app.get("/sensors/{sensor_id}/latest", response_model=schemas.SensorReading)
def get_latest_reading(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return crud.get_latest_reading(db=db, sensor_id=sensor_id)


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


@app.post("/sensors/{sensor_id}", response_model=schemas.SensorReading)
def create_sensor_reading(sensor_id: int, value: float, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return crud.create_sensor_reading(db=db, sensor_id=sensor_id, value=value)
