from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sql_app.crud import canteen
from sql_app.schemas import CanteenItem, CanteenBase, FloorData, FloorStored
from sql_app import get_db
from users import check_admin_privilege

router = APIRouter()


@router.get("/all", response_model=list[CanteenItem])
def get_all_canteen(db=Depends(get_db)):
    return canteen.get_all(db)


@router.get(
    "/campus/{campus_name}",
)
def get_canteen_by_campus(campus_name: str, db=Depends(get_db)):
    return canteen.get_by_campus(db, campus_name)


@router.get("/search/{name}", response_model=list[CanteenItem])
def search_canteen(name: str, db=Depends(get_db)):
    return canteen.search(db, name)


@router.post("", response_model=CanteenItem)
def add_canteen(
    data: CanteenBase, db=Depends(get_db), privilege=Depends(check_admin_privilege)
):
    return canteen.add(db, data)


@router.get("/{canteen_id}", response_model=CanteenItem)
def get_canteen(canteen_id: int, db=Depends(get_db)):
    return canteen.get_info(db, canteen_id)


@router.get("/{cantten_id}/floors", response_model=list[FloorStored])
def get_floors(canteen_id: int, db=Depends(get_db)):
    return canteen.get_floors_info(db, canteen_id)


@router.post("/{canteen_id}/floors", response_model=FloorStored)
def add_floor(
    canteen_id: int,
    data: FloorData,
    db=Depends(get_db),
    privilege=Depends(check_admin_privilege),
):
    return canteen.add_floor(db, floor=data)


@router.delete("/{canteen_id}", response_model=dict[str, str])
def delete_canteen(
    canteen_id: int, db=Depends(get_db), privilege=Depends(check_admin_privilege)
):
    return canteen.delete(db, canteen_id)


@router.put("/{canteen_id}/floors", response_model=dict[str, str])
def update_floor(
    canteen_id: int,
    data: FloorData,
    db=Depends(get_db),
    privilege=Depends(check_admin_privilege),
):
    return canteen.update_floor_info(db, data)


@router.put("", response_model=dict[str, str])
def update_canteen(
    data: CanteenItem, db=Depends(get_db), privilege=Depends(check_admin_privilege)
):
    try:
        return canteen.update(db, data)
    except:
        raise HTTPException(status_code=400, detail="Invalid canteen id")
