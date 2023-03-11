
from sqlalchemy.orm import Session

from . import models, schemas


class ItemRepo:
    
 async def create(db: Session, item: schemas.ItemCreate):
        db_item = models.Item(name=item.name,
                              price=item.price,
                              recipe_id=item.recipe_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
 def fetch_by_id(db: Session,_id):
     return db.query(models.Item).filter(models.Item.id == _id).first()
 
 def fetch_by_name(db: Session,name):
     return db.query(models.Item).filter(models.Item.name == name).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Item).offset(skip).limit(limit).all()
 
 async def delete(db: Session,item_id):
     db_item= db.query(models.Item).filter_by(id=item_id).first()
     db.delete(db_item)
     db.commit()
     
     
 async def update(db: Session,item_data):
    updated_item = db.merge(item_data)
    db.commit()
    return updated_item
    
    
    
class RecipeRepo:
    
    async def create(db: Session, recipe: schemas.RecipeCreate):
        db_recipe = models.Recipe(name=recipe.name,
                                calories=recipe.calories,
                                description=recipe.description,
                                )
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
        
    def fetch_by_id(db: Session,_id:int):
        return db.query(models.Recipe).filter(models.Recipe.id == _id).first()
    
    def fetch_by_name(db: Session,name:str):
        return db.query(models.Recipe).filter(models.Recipe.name == name).first()
    
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Recipe).offset(skip).limit(limit).all()
    
    async def delete(db: Session,_id:int):
        db_recipe= db.query(models.Recipe).filter_by(id=_id).first()
        db.delete(db_recipe)
        db.commit()
        
    async def update(db: Session,recipe_data):
        db.merge(recipe_data)
        db.commit()