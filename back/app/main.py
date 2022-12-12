from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str
    password: str


@app.post("/user/signup")
def signup(user: User):
    return {}


@app.post("/user/login")
def login(user: User):
    return {}


@app.get("/item")
def item_list():
    return {}


@app.get("/item/{item_id}")
def item_detail():
    return {}
