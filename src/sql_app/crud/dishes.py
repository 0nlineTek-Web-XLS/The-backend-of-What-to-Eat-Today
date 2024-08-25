from typing import List
from sqlalchemy.orm import Session

from ..models import Dish
from ..schemas import DishBase, DishItemUpdate, PricingData, AdvancedSearch


def get_all_by_canteen(db: Session, canteen: int, floor: int = 0, window: int = 0, name: str = '' , skip: int = 0, limit: int = 200) -> list[Dish]:
    res = db.query(Dish).filter(Dish.canteen == canteen)
    if floor:
        res = res.filter(Dish.floor == floor)
    if window:
        res = res.filter(Dish.window == window)
    if name:
        res = res.filter(Dish.name == name)
    return res.offset(skip).limit(limit).all()


def add(db: Session, dish: DishBase) -> Dish:
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

def get_by_id(db: Session, dish_id: int) -> Dish | None:
    return db.query(Dish).filter(Dish.id == dish_id).first()

def delete(db: Session, dish_id: int) -> dict[str, str]:
    db.query(Dish).filter(Dish.id == dish_id).delete()
    db.commit()
    return {"detail": "Delete Success"}

def update_price(db: Session, dish_id: int, pricing: PricingData) -> Dish:
    db_dish: Dish | None = db.query(Dish).filter(Dish.id == dish_id).first()
    assert db_dish, "No such dish"
    db_dish.price = pricing.price
    db_dish.measure = pricing.measure
    db.commit()
    return db_dish

def update(db: Session, data: DishItemUpdate) -> Dish:
    db_dish: Dish | None = db.query(Dish).filter(Dish.id == data.id).first() if data.id else None
    assert db_dish, "No such dish"
    db_dish.canteen = data.canteen
    db_dish.floor = data.floor
    db_dish.window = data.window
    db_dish.name = data.name
    db_dish.price = data.price if data.price else db_dish.price
    db_dish.measure = data.measure
    db.commit()
    db.refresh(db_dish)
    return db_dish

def update_image(db: Session, dish_id: int, image: str) -> Dish:
    db_dish: Dish | None = db.query(Dish).filter(Dish.id == dish_id).first()
    assert db_dish, "No such dish"
    db_dish.image = image
    db.commit()
    return db_dish

def search(db: Session, name: str, skip: int = 0, limit: int = 200) -> List[Dish]:
    return db.query(Dish).filter(Dish.name.like(
        f"%{name}%"
    )).offset(skip).limit(limit).all()

def advanced_search(db: Session, data: AdvancedSearch):
    res = db.query(Dish)
    if data.canteen:
        # if not empty list, then filter if id in the list
        res = res.filter(Dish.canteen.in_(data.canteen))
    if data.floor:
        res = res.filter(Dish.floor.in_(data.floor))
    if data.window:
        res = res.filter(Dish.window.in_(data.window))
    if data.name:
        res = res.filter(Dish.name.like(f"%{data.name}%"))
    return res.offset(data.skip).limit(data.limit).all()
