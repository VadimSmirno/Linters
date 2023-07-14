from typing import List, Optional

from pydantic import BaseModel


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
