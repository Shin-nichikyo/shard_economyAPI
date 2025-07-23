from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_shared_id(db: Session, shared_id: str):
    return db.query(models.User).filter(models.User.shared_id == shared_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, shared_id: str, user_data: schemas.UserUpdate):
    db_user = get_user_by_shared_id(db, shared_id)
    if db_user:
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user
