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
from my_app.repositories import IngredientRepo, RecipeRepo

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


@app.post('/ingredients', tags=["Ingredient"], response_model=schemas.Ingredient, status_code=201)
async def create_ingredient(ingredient_request: schemas.IngredientCreate, db: Session = Depends(get_db)):
    """
    Create an Ingredient and recipe it in the database
    """

    db_ingredient = IngredientRepo.fetch_by_name(db, name=ingredient_request.name)
    if db_ingredient:
        raise HTTPException(status_code=400, detail="Ingredient already exists!")

    return await IngredientRepo.create(self=db, ingredient=ingredient_request)


@app.get('/ingredients', tags=["Ingredient"], response_model=List[schemas.Ingredient])
def get_all_ingredient(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    if name:
        ingredients = []
        db_ingredient = IngredientRepo.fetch_by_name(db, name)
        if db_ingredient:
            ingredients.append(db_ingredient)
            return ingredients
        else:
            raise HTTPException(status_code=404, detail=DETAIL_INGREDIENT)
    else:
        return IngredientRepo.fetch_all(db)


@app.get('/ingredients/{ingredient_id}', tags=["Ingredient"], response_model=schemas.Ingredient)
def get_item(ingredient_id: int, db: Session = Depends(get_db)):
    """
    Get the Ingredient with the given ID provided by User stored in database
    """
    db_ingredient = IngredientRepo.fetch_by_id(db, ingredient_id)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail=DETAIL)
    return db_ingredient


@app.delete('/ingredients/{ingredient_id}', tags=["Ingredient"])
async def delete_item(ingredient_id: int, db: Session = Depends(get_db)):
    """
    Delete the Ingredient with the given ID provided by User stored in database
    """
    db_ingredient = IngredientRepo.fetch_by_id(db, ingredient_id)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail=DETAIL)
    await IngredientRepo.delete(db, ingredient_id)
    return "Ingredient deleted successfully!"


@app.put('/ingredients/{ingredient_id}', tags=["Ingredient"], response_model=schemas.Ingredient)
async def update_item(ingredient_id: int, ingredient_request: schemas.Ingredient, db: Session = Depends(get_db)):
    """
    Update an Ingredient stored in the database
    """
    db_ingredient = IngredientRepo.fetch_by_id(db, ingredient_id)
    print(db_ingredient)
    if db_ingredient:
        update_item_encoded = jsonable_encoder(ingredient_request)
        db_ingredient.name = update_item_encoded['name']
        db_ingredient.price = update_item_encoded['price']
        db_ingredient.quantity = update_item_encoded['quantity']
        db_ingredient.recipe_id = update_item_encoded['recipe_id']
        return await IngredientRepo.update(self=db, ingredient_data=db_ingredient)
    else:
        raise HTTPException(status_code=400, detail=DETAIL)


@app.post('/recipes', tags=["Recipe"], response_model=schemas.Recipe, status_code=201)
async def create_recipe(recipe_request: schemas.RecipeCreate, db: Session = Depends(get_db)):
    """
    Create a Recipe and save it in the database
    """
    db_store = RecipeRepo.fetch_by_name(db, name=recipe_request.name)
    print(db_store)
    if db_store:
        raise HTTPException(status_code=400, detail="Recipe already exists!")

    return await RecipeRepo.create(self=db, recipe=recipe_request)


@app.get('/recipes', tags=["Recipe"], response_model=List[schemas.Recipe])
def get_all_stores(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Recipes stored in database
    """
    if name:
        recipes = []
        db_store = RecipeRepo.fetch_by_name(db, name)
        print(db_store)
        recipes.append(db_store)
        return recipes
    else:
        return RecipeRepo.fetch_all(db)


@app.get('/recipes/{recipe_id}', tags=["Recipe"], response_model=schemas.Recipe)
def get_store(recipe_id: int, db: Session = Depends(get_db)):
    """
    Get the Recipe with the given ID provided by User stored in database
    """
    db_store = RecipeRepo.fetch_by_id(db, recipe_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail=DETAIL_RECIPE)
    return db_store


@app.delete('/recipes/{recipe_id}', tags=["Recipe"])
async def delete_store(recipe_id: int, db: Session = Depends(get_db)):
    """
    Delete the Ingredient with the given ID provided by User stored in database
    """
    db_store = RecipeRepo.fetch_by_id(db, recipe_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail=DETAIL_RECIPE)
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