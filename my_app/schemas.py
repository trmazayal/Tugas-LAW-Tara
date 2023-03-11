from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    price: float
    recipe_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    name: str
    calories: float
    description: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True

class Activity(BaseModel):
    activity: str
    type: str
    participants: int
    price: float
    link: str
    key: str
    accessibility: float
