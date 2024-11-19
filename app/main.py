from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import schemas, crud, database, auth

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = auth.get_user(db=db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/visit_request/")
def create_visit_request(request: schemas.VisitRequestCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(db=db, token=token)
    return crud.create_visit_request(db=db, visit_request=request, visitor_id=user.id, visitor_name=user.username)

@app.get("/pending_visits/")
def get_pending_visits(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(db=db, token=token)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view pending visits")
    return crud.get_pending_visits(db=db)

@app.put("/approve_visit/{visit_id}")
def approve_visit(visit_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(db=db, token=token)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can approve visits")
    return crud.approve_visit_request(db=db, visit_id=visit_id)

@app.put("/reject_visit/{visit_id}")
def reject_visit(visit_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(db=db, token=token)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can reject visits")
    return crud.reject_visit_request(db=db, visit_id=visit_id)

@app.get("/security_dashboard/")
def security_dashboard(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(db=db, token=token)
    if user.role != "security":
        raise HTTPException(status_code=403, detail="Only security can view the dashboard")
    
    # Example: View all approved visits for today
    today_visits = crud.get_today_visits(db=db)
    return {"today_visits": today_visits}
