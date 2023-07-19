from typing import List, Optional
from database import async_session
import models
import schemas
from database import engine, session
from fastapi import FastAPI
from flask import jsonify
from log_dir import logger
from models import Ingredient, Recipes
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

app = FastAPI(title="Recepts")

def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def shutdown_up():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_down():
    await session.close()
    await engine.dispose()


@app.get("/recept/{idx}", response_model=schemas.RecipesSchema)
@app.get("/recept", response_model=List[schemas.GetRecipes])
async def get_recept(idx: Optional[int] = None):
    async with session as db:
        if not idx:
            recept = await db.execute(
                select(Recipes).order_by(
                    Recipes.count_view.desc(), Recipes.cooking_time
                )
            )

            recipe_objs = recept.scalars().all()
            recipe_list = []
            for recipe_obj in recipe_objs:
                recipe_dict = {
                    "id": recipe_obj.id,
                    "name": recipe_obj.name,
                    "count_view": recipe_obj.count_view,
                    "cooking_time": recipe_obj.cooking_time,
                }
                recipe_list.append(recipe_dict)
            logger.info(recipe_list)
            return recipe_list
        else:
            get_recept = await db.execute(
                select(Recipes)
                .join(Ingredient)
                .options(joinedload(Recipes.ingredients_list))
                .filter(Recipes.id == idx)
                .order_by(Recipes.count_view.desc(), Recipes.cooking_time)
            )
            recipe_obj = get_recept.scalars().first()
            recipe_obj.count_view += 1
            await db.commit()
            recipe_list = []
            ingredient_list = []
            for ingredient in recipe_obj.ingredients_list:
                ingredient_dict = {"id": ingredient.id, "name": ingredient.name}
                ingredient_list.append(ingredient_dict)

            recipe_dict = {
                "id": recipe_obj.id,
                "name": recipe_obj.name,
                "cooking_time": recipe_obj.cooking_time,
                "descriptions": recipe_obj.descriptions,
                "ingredients_list": ingredient_list,
            }
            recipe_list.append(recipe_dict)
            logger.info(recipe_list)
            return recipe_dict


@app.post("/recept", response_model=schemas.RecipesSchema)
async def create_recept(recept: schemas.RecipesSchema):
    new_recipe = Recipes(
        name=recept.name,
        count_view=recept.count_view,
        cooking_time=recept.cooking_time,
        descriptions=recept.descriptions,
    )
    ingredient = [
        Ingredient(name=ingredient.get("name"), recipe=new_recipe)
        for ingredient in recept.ingredients_list
    ]
    new_recipe.ingredients_list.extend(ingredient)

    async with session as db:
        db.add(new_recipe)
        await db.commit()

    return recept
