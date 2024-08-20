from sqlalchemy.orm import Session

from ..models import Canteen
from ..schemas import CanteenBase, CanteenItem

def get_info(db: Session, canteen_id: int) -> Canteen | None:
    return db.query(Canteen).filter(Canteen.id == canteen_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 200) -> list[Canteen]:
    return db.query(Canteen).offset(skip).limit(limit).all()

def add(db: Session, canteen: CanteenBase) -> Canteen:
    db_canteen = Canteen(name=canteen.name, 
                          description=canteen.description,
                          image=canteen.image, 
                          campus=canteen.campus)
    db.add(db_canteen)
    db.commit()
    db.refresh(db_canteen)
    return db_canteen

def delete(db: Session, canteen_id: int) -> dict[str, str]:
    db.query(Canteen).filter(Canteen.id == canteen_id).delete()
    db.commit()
    return {"detail": "Delete Success"}

def update(db: Session, data: CanteenItem) -> dict[str, str]:
    db_canteen: Canteen | None = db.query(Canteen).filter(Canteen.id == data.id).first() if data.id else None
    assert db_canteen, "No such canteen"
    db_canteen.name = data.name
    db_canteen.description = data.description
    db_canteen.image = data.image if data.image else db_canteen.image
    db.commit()
    return {"detail": "Update Success"}

def get_by_campus(db: Session, campus_name: str) -> list[Canteen]:
    return db.query(Canteen).filter(Canteen.campus == campus_name).all()