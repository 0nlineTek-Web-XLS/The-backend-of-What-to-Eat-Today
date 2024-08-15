from sqlalchemy.orm import Session

from ..models import Dish
from ..schemas import DishBase, DishItem, DishItemPriced, PricingData


def get_all_by_canteen(db: Session, canteen: int, floor: int = 0, window: int = 0, name: str = '' , skip: int = 0, limit: int = 200) -> list[Dish]:
    res = db.query(Dish).filter(Dish.canteen == canteen)
    if floor:
        res = res.filter(Dish.floor == floor)
    if window:
        res = res.filter(Dish.window == window)
    if name:
        res = res.filter(Dish.name == name)
    return res.offset(skip).limit(limit).all()


def add(db: Session, dish: DishItemPriced):
    db_dish = Dish(canteen=dish.canteen, 
                          floor=dish.floor,
                          window=dish.window,
                          name=dish.name,
                          price=dish.price,
                          measure=dish.measure,
                          )
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

def update(db: Session, dish: DishItemPriced):
    db_dish = db.query(Dish).filter(Dish.id == dish.id).first()
    if db_dish is None:
        raise Exception("No such dish")
    if dish.price is not None:
        db_dish.price = dish.price
    db_dish.measure = dish.measure
    db.commit()
    return db_dish

def update_price(db: Session, dish_id: int, pricing: PricingData):
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if db_dish is None:
        raise Exception("No such dish")
    db_dish.price = pricing.price
    db_dish.measure = pricing.measure
    db.commit()
    return db_dish

def update_image(db: Session, dish_id: int, image: bytes):
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if db_dish is None:
        raise Exception("No such dish")
    db_dish.image = image
    db.commit()
    return db_dish

def search(db: Session, name: str, skip: int = 0, limit: int = 200):
    return db.query(Dish).filter(Dish.name.like(f"%{name}%")).offset(skip).limit(limit).all()

