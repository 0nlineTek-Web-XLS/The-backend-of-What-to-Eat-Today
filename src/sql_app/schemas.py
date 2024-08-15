from pydantic import BaseModel


class DishBase(BaseModel):
    canteen: int
    floor: int
    window: int
    name: str
    
class DishPriced(DishBase):
    id: int
    measure: str
    price: float | None = None

class DishItemPriced(DishPriced, DishBase):
    pass

class DishItem(DishItemPriced):
    average_vote: float
    image: bytes | None = None

class CarouselItem(BaseModel):
    canteen: int = 1
    image: bytes
    
class CommentItem(BaseModel):
    user_id: int = 666666
    dish_id: int = 1
    content: str
    vote: int = 3
    time: str = "2024-08-04 12:01:59"



# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True