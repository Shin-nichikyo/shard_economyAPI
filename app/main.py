from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shared Economy API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user/{shared_id}", response_model=schemas.UserOut)
def read_user(shared_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_shared_id(db, shared_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/user", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.patch("/user/{shared_id}", response_model=schemas.UserOut)
def update_user(shared_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, shared_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
