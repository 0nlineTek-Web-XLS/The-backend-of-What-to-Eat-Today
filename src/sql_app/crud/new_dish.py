from sqlalchemy.orm import Session

from ..models import Dish, NewDish


def get(db: Session, canteen: int):
    return db.query(Dish).filter(Dish.canteen == canteen).all()

def delete(db: Session, id: int):
    db.query(Dish).filter(Dish.id == id).delete()
    db.commit()

def add(db: Session, id: int):
    db_dish = db.query(Dish).filter(Dish.id == id).first()
    if db_dish:
        db.add(NewDish(db_dish.id))
        return db_dish

