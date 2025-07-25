from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base

app = FastAPI(title="Shared Economy API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return [
            {
                "id": user.id,
                "universal_id": str(user.universal_id),
                "discord_id": user.discord_id,
                "minecraft_uuid": str(user.minecraft_uuid) if user.minecraft_uuid else None,
                "web_id": user.web_id
            }
            for user in users
        ]
    except Exception as e:
        return {"error": str(e)}

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

# -------------------- LINK ENDPOINTS --------------------
@app.post("/link-code", response_model=schemas.LinkCodeResponse)
def generate_link_code(data: schemas.LinkCodeCreate, db: Session = Depends(get_db)):
    code = crud.create_link_code(db, data.source, data.universal_id)
    return {"code": code}

@app.post("/link")
def link_user(data: schemas.LinkCodeInput, db: Session = Depends(get_db)):
    user = crud.apply_link_code(db, data.code, data.target_type, data.target_id)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid or expired link code")
    return {"message": "Linked successfully", "universal_id": str(user.universal_id)}
