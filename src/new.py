from typing import List
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sql_app.models import Dish
from sql_app.crud import new_dish
from sql_app.schemas import DishItem
from sql_app import get_db
from users import check_admin_privilege
router = APIRouter()

@router.post('', response_model=DishItem)
def add_new_dish(id: int, db = Depends(get_db), privilege = Depends(check_admin_privilege)
                 ) -> new_dish.Dish | None:
    if ret:= new_dish.add(db, id):
        return ret
    else:
        raise HTTPException(status_code=404, detail="No such dish")

@router.get('/{canteen}', response_model=List[DishItem])
def get_new_dish(canteen: int, db = Depends(get_db)) -> List[Dish]:
    return new_dish.get(db, canteen)

@router.delete('/{dish_id}')
def delete_new_dish(dish_id:int, db = Depends(get_db), privilege = Depends(check_admin_privilege)
                    ) -> None:
    return new_dish.delete(db,  dish_id=dish_id)
