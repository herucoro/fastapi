from curses.ascii import HT
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
import models
import schemas
import crud

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}

@app.get("/user/{user_id}", response_model=schemas.UserPublic)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/user/", response_model=List[schemas.UserPublic])
def get_all_user(db: Session = Depends(get_db)):
    db_users = crud.get_all_user(db=db)
    if db_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_users

@app.post("/user/create")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return user

@app.post("/user/{user_id}", response_model=schemas.UserPublic)
def update_user(user: schemas.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/user/{user_id}/delete", response_model=schemas.UserPublic)
def update_user(user: schemas.UserDelete, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)