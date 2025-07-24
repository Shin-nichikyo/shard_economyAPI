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

# --- 連携処理用 ---
class LinkCodeCreate(BaseModel):
    source: str  # discord, minecraft, web
    universal_id: str

class LinkCodeInput(BaseModel):
    code: str
    target_type: str  # discord, minecraft, web
    target_id: str  # discord_id, minecraft_uuid, web_id（全部文字列）

class LinkCodeResponse(BaseModel):
    code: str
