from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .sqlalchemy_conn import Base, engine, get_db
from .models.user import User
from .schemas.user import UserCreate, UserOut
from .workers.process_auth import hash_password, generate_salt
import time

time.sleep(5)
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    salt = generate_salt()
    password_hash = hash_password(payload.password, salt)

    new_user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone_number=payload.phone_number,
        password_hash=password_hash,
        salt=salt
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()
