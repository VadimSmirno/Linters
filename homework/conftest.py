import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, drop_database
from starlette.testclient import TestClient
from main import app, get_db
from database import Base, engine, metadata
from models import Recipes, Ingredient


TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()
    db = Session(bind=connection)
    app.dependency_overrides[get_db] = lambda: db

    recipe = Recipes(
        name="Test Recipe",
        count_view=0,
        cooking_time=30,
        descriptions="Test Description"
    )
    db.add(recipe)
    db.commit()

    ingredient1 = Ingredient(name="Ingredient 1", recipe_id=recipe.id)
    ingredient2 = Ingredient(name="Ingredient 2", recipe_id=recipe.id)
    db.add_all([ingredient1, ingredient2])
    db.commit()

    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
