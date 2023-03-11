from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True,index=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200))
    recipe_id = Column(Integer,ForeignKey('recipes.id'),nullable=False)
    def __repr__(self):
        return 'ItemModel(name=%s, price=%s,recipe_id=%s)' % (self.name, self.price,self.recipe_id)
    
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True)
    items = relationship("Item",primaryjoin="Recipe.id == Item.recipe_id",cascade="all, delete-orphan")

    def __repr__(self):
        return 'Recipe(name=%s)' % self.name