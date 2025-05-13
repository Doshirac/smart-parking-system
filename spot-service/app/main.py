from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .sqlalchemy_conn import Base, engine, get_db
from .models.spot import ParkingSpot
from .schemas.spot import SpotCreate, SpotOut
from .workers.process_spot import handle_spot_status_change
from typing import List, Optional
from datetime import datetime
import time

time.sleep(5)
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/spots", response_model=List[SpotOut])
def list_spots(
    spot_type: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ParkingSpot).filter(ParkingSpot.is_available == True)
    if spot_type:
        query = query.filter(ParkingSpot.spot_type == spot_type)
    if max_price:
        query = query.filter(ParkingSpot.hourly_rate <= max_price)
    return query.all()

@app.get("/spots/{spot_id}", response_model=SpotOut)
def get_spot_by_id(spot_id: int, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.spot_id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot

@app.post("/spots", response_model=SpotOut)
def create_spot(payload: SpotCreate, db: Session = Depends(get_db)):
    new_spot = ParkingSpot(**payload.dict())
    db.add(new_spot)
    db.commit()
    db.refresh(new_spot)
    return new_spot

@app.post("/spots/{spot_id}/block", response_model=SpotOut)
def block_spot(spot_id: int, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.spot_id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    if not spot.is_available:
        raise HTTPException(status_code=400, detail="Spot already blocked")
    spot.is_available = False
    db.commit()
    db.refresh(spot)

    handle_spot_status_change({
        "spot_id": spot.spot_id,
        "is_available": spot.is_available
    })

    return spot
