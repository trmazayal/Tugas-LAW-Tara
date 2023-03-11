from typing import List, Optional
from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    price: float
    quantity: int
    recipe_id: int


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    name: str
    calories: int
    description: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    ingredients: List[Ingredient] = []

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
