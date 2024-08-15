from sqlalchemy.orm import Session

from ..models import Dish
from ..schemas import DishItemPrepared, DishUpdateItem


def get_all_by_canteen(db: Session, canteen: int, floor: int = 0, window: int = 0, name: str = '' , skip: int = 0, limit: int = 200):
    res = db.query(Dish).filter(Dish.canteen == canteen)
    if floor:
        res = res.filter(Dish.floor == floor)
    if window:
        res = res.filter(Dish.window == window)
    if name:
        res = res.filter(Dish.name == name)
    return res.offset(skip).limit(limit).all()


def add(db: Session, dish: DishItemPrepared):
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

def get_by_id(db: Session, dish_id: int):
    return db.query(Dish).filter(Dish.id == dish_id).first()

def delete(db: Session, dish_id: int):
    db.query(Dish).filter(Dish.id == dish_id).delete()
    db.commit()
    return {"detail": "Delete Success"}

def update(db: Session, dish: DishUpdateItem):
    db_dish = db.query(Dish).filter(Dish.id == dish.id).first()
    db.commit()
    return {"detail": "Update Success"}

def search(db: Session, name: str, skip: int = 0, limit: int = 200):
    return db.query(Dish).filter(Dish.name.like(f"%{name}%")).offset(skip).limit(limit).all()

