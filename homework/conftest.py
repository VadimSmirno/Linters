import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database
from starlette.testclient import TestClient
from main import app
from database import Base, engine, metadata
from models import Recipes, Ingredient


@pytest.fixture(scope="session")
def db():
    create_database(engine)
    Base.metadata.create_all(bind=engine)
    yield
    drop_database(engine.url)

@pytest.fixture(scope="function")
def session(db):
    connection = engine.connect()
    session = sessionmaker(bind=connection)()

    recept_data = {
        "name": "Test Recipe",
        "count_view": 0,
        "cooking_time": 30,
        "descriptions": "Test description",
    }
    recipe = Recipes(**recept_data)
    session.add(recipe)
    session.commit()

    ingredient_data = [
        {"name": "Ingredient 1", "recipe_id": recipe.id},
        {"name": "Ingredient 2", "recipe_id": recipe.id},
    ]
    ingredients = [Ingredient(**data) for data in ingredient_data]
    session.add_all(ingredients)
    session.commit()

    yield session

    session.close()
    connection.close()

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client
