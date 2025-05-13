from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .sqlalchemy_conn import Base, engine, get_db
from .models.reservation import Reservation, ReservationStatus
from .schemas.reservation import ReservationCreate, ReservationOut
from .workers.process_reservation import handle_reservation_created
from datetime import datetime
import time
import requests

# Delay for DB readiness
time.sleep(5)
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/reservations", response_model=ReservationOut)
def create_reservation(payload: ReservationCreate, db: Session = Depends(get_db)):
    # Проверка доступности места через spot-service
    spot_resp = requests.get(f"http://spot-service:8000/spots/{payload.spot_id}")
    if spot_resp.status_code != 200 or not spot_resp.json().get("is_available", False):
        raise HTTPException(status_code=400, detail="Spot not available")

    new_res = Reservation(
        user_id=payload.user_id,
        spot_id=payload.spot_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        status=ReservationStatus.pending,
        created_at=datetime.utcnow()
    )
    db.add(new_res)
    db.commit()
    db.refresh(new_res)

    # Отправка события (если нужно)
    handle_reservation_created({
        "reservation_id": new_res.reservation_id,
        "user_id": new_res.user_id,
        "spot_id": new_res.spot_id,
        "start_time": new_res.start_time.isoformat(),
        "end_time": new_res.end_time.isoformat(),
        "status": new_res.status.value
    })

    return new_res

@app.post("/confirm")
def confirm_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter_by(reservation_id=reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    reservation.status = ReservationStatus.confirmed
    db.commit()

    # Изменяем статус места на false через spot-service
    requests.patch(f"http://spot-service:8000/spots/{reservation.spot_id}", json={"is_available": False})

    return {"message": "Reservation confirmed"}

@app.get("/reservations/{reservation_id}", response_model=ReservationOut)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation