from sqlalchemy import Column, Integer, BigInteger, String, Date, TIMESTAMP, Float, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    universal_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    discord_id = Column(BigInteger, unique=True, nullable=True)
    minecraft_uuid = Column(UUID(as_uuid=True), unique=True, nullable=True)
    web_id = Column(String, unique=True, nullable=True)

class Economy(Base):
    __tablename__ = "economy"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.universal_id"), primary_key=True)
    balance = Column(Integer, default=0)
    activity_score = Column(Float, default=100.0)
    level = Column(Integer, default=1)
    last_active_date = Column(Date)
    last_work_time = Column(TIMESTAMP)

class LinkCode(Base):
    __tablename__ = "link_codes"

    code = Column(String(6), primary_key=True, index=True)
    source = Column(String, nullable=False)  # "discord", "minecraft", "web"
    universal_id = Column(UUID(as_uuid=True), ForeignKey("users.universal_id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
