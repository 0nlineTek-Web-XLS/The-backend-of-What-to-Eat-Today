from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
import dish
import users
import canteen
import new
import carousel
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from random import choice
from typing import List
# from fastapi.staticfiles import StaticFiles
import dish
import pandas as pd
import uvicorn

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

app = FastAPI()

# app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")
app.include_router(dish.router, prefix="/dish", tags=["dish"])
app.include_router(canteen.router, prefix="/canteen", tags=["canteen"])
app.include_router(new.router, prefix="/new", tags=["new"])
app.include_router(carousel.router, prefix="/carousel", tags=["carousel"])
app.include_router(users.router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
