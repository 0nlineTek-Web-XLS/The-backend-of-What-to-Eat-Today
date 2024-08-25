from sqlalchemy.orm import Session

from ..models import Canteen
from ..schemas import CanteenBase, CanteenItem

def get_info(db: Session, canteen_id: int) -> Canteen | None:
    """
    Get the information of a canteen by its id.
    """
    return db.query(Canteen).filter(Canteen.id == canteen_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 200) -> list[Canteen]:
    """
    Get all canteens.
    """
    return db.query(Canteen).offset(skip).limit(limit).all()

def add(db: Session, canteen: CanteenBase) -> Canteen:
    """
    Add a canteen.
    """
    db_canteen = Canteen(name=canteen.name, 
                          description=canteen.description,
                          image=canteen.image, 
                          campus=canteen.campus)
    db.add(db_canteen)
    db.commit()
    db.refresh(db_canteen)
    return db_canteen

def delete(db: Session, canteen_id: int) -> dict[str, str]:
    """
    Delete a canteen by its id.
    """
    db.query(Canteen).filter(Canteen.id == canteen_id).delete()
    db.commit()
    return {"detail": "Delete Success"}

def update(db: Session, data: CanteenItem) -> dict[str, str]:
    """
    Update a canteen.
    """
    db_canteen: Canteen | None = db.query(Canteen).filter(Canteen.id == data.id).first() if data.id else None
    assert db_canteen, "No such canteen"
    db_canteen.name = data.name
    db_canteen.description = data.description
    db_canteen.image = data.image if data.image else db_canteen.image
    db.commit()
    return {"detail": "Update Success"}

def get_by_campus(db: Session, campus_name: str) -> list[Canteen]:
    """
    Get all canteens in a campus.
    """
    return db.query(Canteen).filter(Canteen.campus == campus_name).all()
