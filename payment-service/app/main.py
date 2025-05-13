from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .sqlalchemy_conn import Base, engine, get_db
from .models.transaction import Transaction, TransactionStatus, PaymentMethod
from .schemas.transaction import TransactionCreate, TransactionOut
from datetime import datetime
import time
import requests

# Delay for DB readiness
time.sleep(5)
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/transactions", response_model=TransactionOut)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    new_tx = Transaction(
        reservation_id=payload.reservation_id,
        user_id=payload.user_id,
        amount=payload.amount,
        payment_method=payload.payment_method,
        status=TransactionStatus.pending,
        created_at=datetime.utcnow()
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)

    # Имитация успешной оплаты
    new_tx.status = TransactionStatus.completed
    new_tx.paid_at = datetime.utcnow()
    db.commit()

    # Подтверждение брони
    requests.post("http://reservation-service:8000/confirm", params={"reservation_id": payload.reservation_id})

    return new_tx

@app.get("/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction