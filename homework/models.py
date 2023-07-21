from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Recipes(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    count_view = Column(Integer)
    cooking_time = Column(Integer)
    descriptions = Column(Text)
    ingredients_list = relationship("Ingredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipes", back_populates="ingredients_list")
