from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sql_app.crud import carousel 
from sql_app import get_db
from users import check_admin_privilege
router = APIRouter()

@router.post('')
def add_carousel(item: carousel.CarouselItem, db = Depends(get_db), privilege = Depends(check_admin_privilege)
                 ):
    return carousel.add(db, item)

@router.get('/{canteen}')
def get_carousel(canteen: int, db = Depends(get_db), ):
    return carousel.get(db, canteen)

@router.delete('')
def delete_carousel(item: carousel.CarouselItem, db = Depends(get_db), privilege = Depends(check_admin_privilege)
                    ):
    return carousel.delete(db, item)

