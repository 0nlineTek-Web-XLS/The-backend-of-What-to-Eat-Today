from sqlalchemy.orm import Session

from ..models import Dish
from ..schemas import DishItem, DishUpdateItem


def get(db: Session, canteen: int):
    return db.query(Dish).filter(Dish.canteen == canteen).all()

def delete(db: Session, id: int):
    db.query(Dish).filter(Dish.id == id).delete()
    db.commit()

def add(db: Session, dish: DishItem):
    db_dish = Dish(canteen=dish.canteen, 
                          floor=dish.floor,
                          window=dish.window,
                          name=dish.name,
                          price=dish.price,
                          measure=dish.measure,
                          image=dish.image)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish
