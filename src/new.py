from fastapi import APIRouter, Depends, UploadFile, HTTPException

from sql_app.crud import new_dish
from sql_app import get_db

router = APIRouter()

@router.post('')
def add_new_dish(id: int, db = Depends(get_db)):
    return new_dish.add(db, id)

@router.get('/{canteen}')
def get_new_dish(canteen: int, db = Depends(get_db)):
    return new_dish.get(db, canteen)

@router.delete('/{id}')
def delete_new_dish(id:int, db = Depends(get_db)):
    return new_dish.delete(db,  id= id)
