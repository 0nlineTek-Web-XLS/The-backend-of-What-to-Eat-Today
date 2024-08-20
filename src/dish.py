from sql_app.crud.dishes import *
from sql_app.models import Dish
from sql_app.schemas import DishItem, DishBase, PricingData, DishItemUpdate, AdvancedSearch
from sql_app import get_db
from sql_app.crud.canteen import get_all
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse
import random
import pandas as pd
from users import check_admin_privilege

router = APIRouter()


@router.get("/{canteen}/all", response_model=list[DishItem])
def get_dish_by_canteen(canteen: int, db: Session = Depends(get_db)) -> list[Dish]:
    return get_all_by_canteen(db, canteen)


@router.get("/{canteen}/{floor}/all", response_model=list[DishItem])
def get_dish_by_floor(
    canteen: int, floor: int, db: Session = Depends(get_db)
) -> list[Dish]:
    return get_all_by_canteen(db, canteen, floor)


@router.get("/{canteen}/{floor}/{window}", response_model=list[DishItem])
def get_dish_by_window(
    canteen: int, floor: int, window: int, db: Session = Depends(get_db)
) -> list[Dish]:
    return get_all_by_canteen(db, canteen, floor, window)


@router.post("", response_model=DishBase)
def add_dish(dish: DishBase, 
             db: Session = Depends(get_db),
             privileged = Depends(check_admin_privilege),
             ) -> Dish:
    return add(db, dish)


@router.put("", response_model=DishItem)
def update_dish(dish: DishItemUpdate, db: Session = Depends(get_db), privileged = Depends(check_admin_privilege)) -> Dish:
    return update(db, dish)


@router.patch("/{dish_id}/pricing", response_model=DishItem)
def update_dish_pricing(
    dish_id: int, pricing: PricingData, db: Session = Depends(get_db), privileged = Depends(check_admin_privilege)
) -> Dish:
    return update_price(db, dish_id, pricing)


@router.patch("/{dish_id}/image", response_model=DishItem)
def update_dish_image(
    dish_id: int, image: UploadFile, db: Session = Depends(get_db), privileged = Depends(check_admin_privilege)
) -> Dish:
    # check if valid image
    try:
        assert image.content_type.startswith("image")  # type: ignore
    except:
        raise HTTPException(status_code=400, detail="Invalid image")
    return update_image(db, dish_id, image.file.read())


@router.delete("", deprecated=True)
def delete_dish(dish: DishBase, db: Session = Depends(get_db), privileged = Depends(check_admin_privilege)
                ) -> dict[str, str]:
    """
    It is a stupid API which filters the dish by name and canteen and floor and other info but JUST NO ID

    Delete it

    **To be deprecated** as the function consumes too much time while filtering the dish by all the info simply to get the id
    """
    try:
        id = get_all_by_canteen(db, dish.canteen, dish.floor, dish.window, dish.name)
        assert len(id) == 1
        id = id[0].id
        return delete(db, id)
    except:
        raise HTTPException(422, detail="No such dish")


@router.delete("/{dish_id}")
def delete_dish_by_id(dish_id: int, db: Session = Depends(get_db), privileged = Depends(check_admin_privilege)
                      ) -> dict[str, str]:
    try:
        return delete(db, dish_id)
    except:
        raise HTTPException(422, detail="No such dish")


@router.get("/{dish_id}", response_model=DishItem)
def get_dish_by_id(dish_id: int, db: Session = Depends(get_db)) -> Dish:
    ret = get_by_id(db, dish_id)
    if ret is None:
        raise HTTPException(404, detail="Dish Not found")
    return ret


@router.get("/{canteen}/random", response_model=DishItem)
def get_random_dish(canteen: int, db: Session = Depends(get_db)) -> Dish:
    try:
        return random.choice(get_all_by_canteen(db, canteen))
    except:
        raise HTTPException(422, detail="Invalid input")


@router.get("/search/", response_model=list[DishItem])
def search_dish_by_name_alike(
    s: str, skip: int, limit: int, db: Session = Depends(get_db)
) -> list[Dish]:
    return search(db, s, skip=skip, limit=limit)

@router.post("/search/advanced", response_model=list[DishItem])
def advanced_search_dish(
    data: AdvancedSearch, db: Session = Depends(get_db)
) -> list[Dish]:
    return advanced_search(db, data)


@router.get("/excel/sample", response_class=FileResponse)
def get_excel_sample(
    privileged = Depends(check_admin_privilege)
) -> FileResponse:
    return FileResponse("sample.xlsx")


@router.post("/excel", response_model=list[DishItem])
def upload_excel(file: UploadFile, db: Session = Depends(get_db), privileged = Depends(check_admin_privilege)
                 ) -> list[Dish]:
    try:
        df = pd.read_excel(file.file)
    except:
        raise HTTPException(400, detail="Invalid Excel File")
    data_dict = df.to_dict("records")
    canteen_dict = {i.name: i.id for i in get_all(db)}
    # print(canteen_dict)
    ret:list[Dish] = []
    for dicts in data_dict:
        dish_item: DishBase=DishBase(
                canteen=canteen_dict[dicts["食堂"]],
                floor=dicts["楼层"],
                window=dicts["窗口"],
                name=dicts["菜品"],
                measure=dicts["单位"],
                price=dicts["价格"],
            )
        
        ret.append(add_dish(
            dish_item,
            db,
        ))

    return ret
