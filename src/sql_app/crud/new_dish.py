from sqlalchemy.orm import Session

from ..models import Dish
from ..schemas import DishItem, DishUpdateItem


def get(db: Session, canteen: int):
    return db.query(Dish).filter(Dish.canteen == canteen).all()

def delete(db: Session, id: int):
    db.query(Dish).filter(Dish.id == id).delete()
    db.commit()

def add(db: Session, id: int):

    db_dish = db.query(Dish).filter(Dish.id == id).first()
    if db_dish:
        return db_dish

