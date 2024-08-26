from typing import List, Tuple
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session

from ..models import Dish, NewDish


def get(db: Session, canteen: int):
    # return Dish whose canteen is canteen and its id in table NewDish
    return db.query(Dish).join(NewDish, Dish.id == NewDish.dish_id).filter(Dish.canteen == canteen).all()

def delete(db: Session, dish_id: int):
    db.query(NewDish).filter(NewDish.dish_id == dish_id).delete()
    db.commit()
    return {
        "status": "success"
    }

def add(db: Session, dish_id: int) -> Dish | None:
    db_dish: Dish | None = db.query(Dish).filter(Dish.id == dish_id).first()
    if db_dish:
        db.add(NewDish(
            dish_id=dish_id
        ))
    db.commit()
    db.refresh(db_dish)
    return db_dish
