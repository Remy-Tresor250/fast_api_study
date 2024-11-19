from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app import models, schemas
from app.auth import get_password_hash
from datetime import date

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_visit_request(db: Session, visit_request: schemas.VisitRequestCreate, visitor_id: int, visitor_name: str):
    db_visit_request = models.VisitRequest(
        visitor_name=visitor_name,
        visit_date=visit_request.visit_date,
        visit_time_from=visit_request.visit_time_from,
        visit_time_to=visit_request.visit_time_to,
        user_id=visitor_id,
    )
    db.add(db_visit_request)
    db.commit()
    db.refresh(db_visit_request)
    return db_visit_request

def get_pending_visits(db: Session):
    return db.query(models.VisitRequest).filter(models.VisitRequest.status == "pending").all()

def approve_visit_request(db: Session, visit_id: int):
    db_visit = db.query(models.VisitRequest).filter(models.VisitRequest.id == visit_id).first()
    if db_visit:
        db_visit.status = "approved"
        db.commit()
        db.refresh(db_visit)
    return db_visit

def reject_visit_request(db: Session, visit_id: int):
    db_visit = db.query(models.VisitRequest).filter(models.VisitRequest.id == visit_id).first()
    if db_visit:
        db_visit.status = "rejected"
        db.commit()
        db.refresh(db_visit)
    return db_visit

def get_today_visits(db: Session):
    today = date.today()
    return db.query(models.VisitRequest).filter(
        func.date(models.VisitRequest.visit_date) == today,
        models.VisitRequest.status == "approved"
    ).all()