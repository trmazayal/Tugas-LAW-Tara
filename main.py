import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import activity
import time
import asyncio

import my_app.models as models
import my_app.schemas as schemas
from db import get_db, engine
from my_app.repositories import ItemRepo, RecipeRepo

app = FastAPI(title="Tugas Mandiri 1 - LAW 2023",
              description="Tara Mazaya Lababan - 2006473535",
              version="1.0.0", )

models.Base.metadata.create_all(bind=engine)

DETAIL_INGREDIENT = "Ingredient not found"
DETAIL_RECIPE = "Recipe not found"

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    context = {"message": f"{base_error_message}. Detail: {err}"}
    return JSONResponse(status_code=400,content=context)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


@app.post('/items', tags=["Item"], response_model=schemas.Item, status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create an Item and store it in the database
    """

    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await ItemRepo.create(db=db, item=item_request)


@app.get('/items', tags=["Item"], response_model=List[schemas.Item])
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    if name:
        items = []
        db_item = ItemRepo.fetch_by_name(db, name)
        items.append(db_item)
        return items
    else:
        return ItemRepo.fetch_all(db)


@app.get('/items/{item_id}', tags=["Item"], response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item


@app.delete('/items/{item_id}', tags=["Item"])
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db, item_id)
    return "Item deleted successfully!"


@app.put('/items/{item_id}', tags=["Item"], response_model=schemas.Item)
async def update_item(item_id: int, item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.price = update_item_encoded['price']
        db_item.description = update_item_encoded['description']
        db_item.recipe_id = update_item_encoded['recipe_id']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")


@app.post('/recipes', tags=["Recipe"], response_model=schemas.Recipe, status_code=201)
async def create_recipe(recipe_request: schemas.RecipeCreate, db: Session = Depends(get_db)):
    """
    Create a Recipe and save it in the database
    """
    db_recipe = RecipeRepo.fetch_by_name(db, name=recipe_request.name)
    print(db_recipe)
    if db_recipe:
        raise HTTPException(status_code=400, detail="Recipe already exists!")

    return await RecipeRepo.create(db=db, recipe=recipe_request)


@app.get('/recipes', tags=["Recipe"], response_model=List[schemas.Recipe])
def get_all_recipes(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Recipes stored in database
    """
    if name:
        recipes = []
        db_recipe = RecipeRepo.fetch_by_name(db, name)
        print(db_recipe)
        recipes.append(db_recipe)
        return recipes
    else:
        return RecipeRepo.fetch_all(db)


@app.get('/recipes/{recipe_id}', tags=["Recipe"], response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Get the Recipe with the given ID provided by User stored in database
    """
    db_recipe = RecipeRepo.fetch_by_id(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found with the given ID")
    return db_recipe


@app.delete('/recipes/{recipe_id}', tags=["Recipe"])
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_recipe = RecipeRepo.fetch_by_id(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found with the given ID")
    await RecipeRepo.delete(db, recipe_id)
    return "Recipe deleted successfully!"


@app.get("/activities/", tags=["Activity"])
def get_activities() -> dict:
    """
    Return the random activities
    """
    return activity.get_my_activity()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)