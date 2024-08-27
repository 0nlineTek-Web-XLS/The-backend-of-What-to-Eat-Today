from sqlalchemy.sql.expression import and_
from sqlalchemy.orm import Session

from ..models import Canteen, Floor
from ..schemas import CanteenBase, CanteenItem, FloorData

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
                          campus=canteen.campus,
                          icon=canteen.icon,
                            floors_count=canteen.floors_count)
    

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
    db_canteen.image = data.image
    db_canteen.icon = data.icon
    db_canteen.floors_count = data.floors_count
    db.commit()
    return {"detail": "Update Success"}

def get_by_campus(db: Session, campus_name: str) -> list[Canteen]:
    """
    Get all canteens in a campus.
    """
    return db.query(Canteen).filter(Canteen.campus == campus_name).all()

def search(db: Session, name: str) -> list[Canteen]:
    """
    Search canteens by name.
    """
    return db.query(Canteen).filter(Canteen.name.like(f"%{name}%")).all()

def get_floors_info(db: Session, canteen_id: int) -> list[Floor]:
    """
    Get the floors information of a canteen.
    """
    return db.query(Floor).filter(Floor.canteen == canteen_id).all()

def update_floor_info(db: Session, floor: FloorData) -> dict[str, str]:
    """
    Update the information of a floor.
    """
    db_floor: Floor | None = db.query(Floor).filter(and_(Floor.canteen == floor.canteen, Floor.floor_in_canteen == floor.floor)).first()
    assert db_floor, "No such floor"
    db_floor.count_of_windows = floor.count_of_windows
    db.commit()
    return {"detail": "Update Success"}

def add_floor(db: Session, floor: FloorData) -> Floor:
    """
    Add the information of a floor.
    """
    db_floor = Floor(canteen=floor.canteen, 
                     floor_in_canteen=floor.floor, 
                     count_of_windows=floor.count_of_windows)
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor
