from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="visitor")
    visit_requests = relationship("VisitRequest", back_populates="user", cascade="all, delete-orphan")

class VisitRequest(Base):
    __tablename__ = "visit_requests"

    id = Column(Integer, primary_key=True, index=True)
    visitor_name = Column(String, nullable=False)
    visit_date = Column(DateTime, nullable=False)
    visit_time_from = Column(DateTime, nullable=False)
    visit_time_to = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="visit_requests")
