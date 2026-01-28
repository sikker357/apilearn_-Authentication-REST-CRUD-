# ...existing code...
from fastapi import FastAPI, Request, Depends, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os
from datetime import timedelta

from . import models, crud, schemas
from .database import engine
from .auth import get_db, get_current_user, create_access_token, verify_password

load_dotenv()

app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Config
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# CORS
origins = [
    "http://localhost:3000",
    "https://your-frontend-domain.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple request logger middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print("response sent back")
    return response

@app.get("/", summary="Health check")
def root():
    return {"message": "Hello World"}

# Background logger helper
def write_log(message: str):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

# Signup
@app.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db=Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db, user)

# Token (login)
@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Current user
@app.get("/users/me", response_model=schemas.UserOut)
def read_me(current_user = Depends(get_current_user)):
    return current_user

# Todos (DB-backed)
# NOTE: changed routes to match frontend calls (no trailing slash)
@app.post("/todos", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db=Depends(get_db), current_user = Depends(get_current_user)):
    return crud.create_todo(db, todo, current_user.id)

@app.get("/todos", response_model=list[schemas.TodoOut])
def read_todos(db=Depends(get_db), current_user = Depends(get_current_user)):
    return crud.get_todos(db, current_user.id)
# ...existing code..