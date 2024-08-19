from pydantic import BaseModel

from datetime import datetime
class DishBase(BaseModel):
    """
    DishBase is the base class for a dish item.

    All dish items should belong to a window in a floor in a canteen.

    Attributes:
    canteen: int
    floor: int
    window: int
    name: str
    measure: str = '份'
    price: float | None = None
    
    """
    canteen: int
    floor: int
    window: int
    name: str
    measure: str = '份'
    price: float | None = None

class DishItemUpdate(DishBase):
    """
    DishItemStored is the class for a dish item stored in the database.

    Attributes:
    id: int
    canteen: int
    floor: int
    window: int
    name: str
    measure: str = '份'
    price: float | None = None
    """
    id: int
class DishItem(DishItemUpdate):
    """
    DishItem is the class for a dish item returned to the client. It includes all the attributes of DishItemStored and some additional attributes.

    Attributes:
    id: int
    canteen: int
    floor: int
    window: int
    name: str
    measure: str = '份'
    price: float | None = None
    average_vote: float
    image: bytes = b''
    """
    average_vote: float
    image: bytes = b''
class PricingData(BaseModel):
    """
    PricingData is the class for the pricing data of a dish item. It is used to update the price of a dish item.

    Attributes:
    price: float
    measure: str = '份'

    For example, if you want to update the price of a dish item with id 1 to 10.5 yuan per 份, you can use PricingData(id=1, price=10.5).
    """
    price: float
    measure: str = '份'

class CarouselItem(BaseModel):
    """
    CarouselItem is the class for a carousel item.

    Attributes:
    canteen: int
    image: bytes = b''
    """
    canteen: int = 1
    image: bytes = b''
    
class CommentItem(BaseModel):
    """
    CommentItem is the class for a comment item.
    """
    user_id: int 
    dish_id: int 
    content: str
    vote: int = 3
    time: datetime = datetime.now()

class CommentStored(CommentItem):
    """
    CommentStored is the class for a comment item stored in the database.
    """
    id: int

class CanteenBase(BaseModel):
    """
    CanteenBase is the base class for a canteen item.

    Attributes:
    name: str
    description: str
    image: bytes = b''
    campus: str
    """
    name: str
    description: str
    image: bytes = b''
    campus: str

class CanteenItem(CanteenBase):
    """
    CanteenItemStored is the class for a canteen item stored in the database.

    Attributes:
    id: int
    name: str
    description: str
    image: bytes = b''
    campus: str
    """
    id: int

class AdvancedSearch(BaseModel):
    """
    AdvancedSearchItem is the class for the advanced search item.

    Attributes:
    canteen: int | None = None
    floor: int | None = None
    window: int | None = None
    name: str | None = None
    """
    canteen: list[int] = []
    floor: list[int] = []
    window: list[int] = []
    name: str = ''
    skip: int = 0
    limit: int = 200