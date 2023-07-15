from sqlalchemy.orm import sessionmaker
from database import Base
import pytest
from sqlalchemy import create_engine
from models import Recipes, Ingredient


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine('sqlite:///:memory:')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Добавление тестовых данных
    recipe1 = Recipes(name="Recipe 1", count_view=10, cooking_time=30, descriptions="Description 1")
    ingredient1 = Ingredient(name="Ingredient 1", recipe=recipe1)
    session.add(recipe1)
    session.commit()

    yield session

    Base.metadata.drop_all(engine)
    session.close()
