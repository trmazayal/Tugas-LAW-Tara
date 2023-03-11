from sqlalchemy.orm import Session
from . import models, schemas

class IngredientRepo:
    
    async def create(self: Session, ingredient: schemas.IngredientCreate):
        self_ingredient = models.Ingredient(
            recipe_id=ingredient.recipe_id,
            name=ingredient.name,
            price=ingredient.price,
            quantity=ingredient.quantity
        )
        self.add(self_ingredient)
        self.commit()
        self.refresh(self_ingredient)
        return self_ingredient
    
    def fetch_by_id(self: Session,_id):
        return self.query(models.Ingredient).filter(models.Ingredient.id == _id).first()
 
    def fetch_by_name(self: Session,name):
        return self.query(models.Ingredient).filter(models.Ingredient.name.ilike(name)).first()
 
    def fetch_all(self: Session, skip: int = 0, limit: int = 100):
        return self.query(models.Ingredient).offset(skip).limit(limit).all()
 
    async def delete(self: Session, ingredient_id):
        self_ingredient= self.query(models.Ingredient).filter_by(id=ingredient_id).first()
        self.delete(self_ingredient)
        self.commit()
     
    async def update(self: Session,ingredient_data):
        updated_ingredient = self.merge(ingredient_data)
        self.commit()
        return updated_ingredient
    
    
    
class RecipeRepo:
    
    async def create(self: Session, recipe: schemas.RecipeCreate):
        self_recipe = models.Recipe(name=recipe.name,
                                    calories=recipe.calories,
                                    description=recipe.description)
        self.add(self_recipe)
        self.commit()
        self.refresh(self_recipe)
        return self_recipe
        
    def fetch_by_id(self: Session,_id:int):
        return self.query(models.Recipe).filter(models.Recipe.id == _id).first()
    
    def fetch_by_name(self: Session,name:str):
        return self.query(models.Recipe).filter(models.Recipe.name == name).first()
    
    def fetch_all(self: Session, skip: int = 0, limit: int = 100):
        return self.query(models.Recipe).offset(skip).limit(limit).all()
    
    async def delete(self: Session,_id:int):
        self_recipe= self.query(models.Recipe).filter_by(id=_id).first()
        self.delete(self_recipe)
        self.commit()
        
    async def update(self: Session,recipe_data):
        self.merge(recipe_data)
        self.commit()