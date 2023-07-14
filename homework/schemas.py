from datetime import time
from pydantic import BaseModel, Field
from typing import List, Optional
from models import Ingredient


class IngredientSchema(BaseModel):
    id: int
    name: str
    recipe_id: int


class RecipesSchema(BaseModel):
    id: int
    name: str
    count_view: Optional[int]
    cooking_time: int
    descriptions: str
    ingredients_list: List


class GetRecipes(BaseModel):
    id: Optional[int]
    name: str
    count_view: int
    cooking_time: int
