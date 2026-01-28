# apilearn/schemas.py
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    owner_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True