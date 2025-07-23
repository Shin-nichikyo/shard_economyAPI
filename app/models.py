from sqlalchemy import Column, Integer, String, BigInteger, TIMESTAMP, func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    shared_id = Column(String, unique=True, index=True)
    username = Column(String)
    currency = Column(BigInteger, default=0)
    activity_score = Column(Integer, default=100)
    level = Column(Integer, default=1)
    last_active = Column(TIMESTAMP, default=func.now())
