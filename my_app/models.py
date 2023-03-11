from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base
    
class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True,index=True)
    recipe_id = Column(Integer,ForeignKey('recipes.id'),nullable=False)
    name = Column(String(80), nullable=False, unique=True,index=True)
    price = Column(Float(precision=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    def __repr__(self):
        return 'IngredientModel(recipe_id=%s, name=%s, price=%s, quantity=%s)' % (self.recipe_id, 
                                                                                  self.name, 
                                                                                  self.price, 
                                                                                  self.quantity)
    
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True)
    calories = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    Ingredients = relationship("Ingredient",
                         primaryjoin="Recipe.id == Ingredient.recipe_id",
                         cascade="all, delete-orphan")

    def __repr__(self):
        return 'Recipe(name=%s, calories=%s, description=%s)' % (self.name, 
                                                                 self.calories, 
                                                                 self.description)