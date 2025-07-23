from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    shared_id: str
    username: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    currency: int | None = None
    activity_score: int | None = None
    level: int | None = None

class UserOut(UserBase):
    currency: int
    activity_score: int
    level: int
    last_active: datetime

    class Config:
        orm_mode = True
