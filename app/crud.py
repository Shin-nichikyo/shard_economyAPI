from sqlalchemy.orm import Session
from . import models, schemas
import datetime
import random
import string
from sqlalchemy import or_

def get_user_by_shared_id(db: Session, shared_id: str):
    return db.query(models.User).filter(models.User.universal_id == shared_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        universal_id=user.shared_id,
        discord_id=int(user.username) if user.username.isdigit() else None  # テスト用途
    )
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

# ------------------------ Link Code ------------------------
def generate_code(n=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def create_link_code(db: Session, source: str, universal_id):
    code = generate_code()
    db_code = models.LinkCode(
        code=code,
        source=source,
        universal_id=universal_id,
        created_at=datetime.datetime.utcnow()
    )
    db.add(db_code)
    db.commit()
    return code

def get_link_code(db: Session, code: str):
    return db.query(models.LinkCode).filter(models.LinkCode.code == code).first()

def apply_link_code(db: Session, code: str, target_type: str, target_id: str):
    link = get_link_code(db, code)
    if not link:
        return None

    # 同一IDをもつユーザーが他にいないかチェックしてマージする
    existing_user = db.query(models.User).filter(
        or_(
            models.User.discord_id == int(target_id) if target_type == "discord" else False,
            models.User.minecraft_uuid == target_id if target_type == "minecraft" else False,
            models.User.web_id == target_id if target_type == "web" else False,
        )
    ).first()

    if existing_user and existing_user.universal_id != link.universal_id:
        # 統合処理
        base = db.query(models.Economy).filter_by(user_id=link.universal_id).first()
        duplicate = db.query(models.Economy).filter_by(user_id=existing_user.universal_id).first()
        if base and duplicate:
            base.balance += duplicate.balance
            base.activity_score += duplicate.activity_score
            db.delete(duplicate)
        db.delete(existing_user)

    # 紐付け
    user = db.query(models.User).filter_by(universal_id=link.universal_id).first()
    if target_type == "discord":
        user.discord_id = int(target_id)
    elif target_type == "minecraft":
        user.minecraft_uuid = target_id
    elif target_type == "web":
        user.web_id = target_id
    db.delete(link)
    db.commit()
    db.refresh(user)
    return user
