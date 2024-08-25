from ..schemas import MarkCreate, MarkData
from sqlalchemy.orm import Session
from ..models import Mark, Dish

def add(db: Session, mark: MarkCreate):
    db_mark = Mark(
        user_id = mark.user_id,
        dish_id = mark.dish_id,
        time = mark.time,
    )
    db.query(Dish).filter(Dish.id == mark.dish_id).update({"count_of_mark": Dish.count_of_mark + 1})
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark

def get_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Mark).filter(Mark.user_id == user_id).offset(skip).limit(limit=limit).all()
def get_by_id(db: Session, mark_id: int):
    return db.query(Mark).filter(Mark.id == mark_id).first()

def delete(db: Session, mark_id: int, uid: int):
    k: Mark | None = db.query(Mark).filter(Mark.id == mark_id).first()
    if k is None:
        return None
    if k.user_id != uid:
        raise ValueError('Unauthorized')
    dish_id = k.dish_id
    db.delete(k)
    db.query(Dish).filter(Dish.id == dish_id).update({"count_of_mark": Dish.count_of_mark - 1})
    db.commit()
    return True

def get_by_dish(db: Session, dish_id: int, skip: int = 0, limit: int = 100):
    return db.query(Mark).filter(Mark.dish_id == dish_id).offset(skip).limit(limit=limit).count()