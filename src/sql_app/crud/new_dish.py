from sqlalchemy.orm import Session

from ..models import Dish, NewDish


def get(db: Session, canteen: int):
    return db.query(Dish).filter(Dish.canteen == canteen).all()

def delete(db: Session, dish_id: int):
    db.query(Dish).filter(Dish.id == dish_id).delete()
    db.commit()

def add(db: Session, dish_id: int) -> Dish | None:
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if db_dish:
        db.add(NewDish(
            dish_id=id
        ))
        return db_dish

