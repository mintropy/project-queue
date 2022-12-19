from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/signup")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=404)
    return crud.create_user(db=db, user=user)


@app.post("/user/login")
def login(user):
    return {}


@app.get("/item")
def item_list():
    return {}


@app.get("/item/{item_id}")
def item_detail():
    return {}
