from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "0ce050565cb9535ed86717bf3b24d5400870fe86ea3b03995cd47e9b6e8add5b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


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
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    username, password = user.username, user.password
    db_user = crud.get_user(db, username)
    if db_user and db_user.password == password:
        return "JWT_token"
    return HTTPException(status_code=401)


@app.get("/item")
def item_list():
    return {}


@app.get("/item/{item_id}")
def item_detail():
    return {}
