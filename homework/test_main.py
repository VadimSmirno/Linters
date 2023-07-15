from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_number():
    assert 1 == 1

def test_get_all_recepts():
    response = client.get("/recept")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recept_by_id():
    response = client.get("/recept/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_recept_by_invalid_id():
    response = client.get("/recept/invalid_id")
    assert response.status_code == 422


def test_create_recept():
    recept_data = {
        "id": 1,
        "name": "суп",
        "count_view": 0,
        "cooking_time": 40,
        "descriptions": "вкусный",
        "ingredients_list": [
            {"id": 3, "name": "морковь", "recipe_id": 1},
            {"id": 4, "name": "свекла", "recipe_id": 1},
        ],
    }
    response = client.post("/recept", json=recept_data)
    assert response.json()["name"] == recept_data["name"]
    assert response.json()["count_view"] == recept_data["count_view"]
    assert response.json()["cooking_time"] == recept_data["cooking_time"]
    assert response.json()["descriptions"] == recept_data["descriptions"]
    assert len(response.json()["ingredients_list"]) == len(
        recept_data["ingredients_list"]
    )


def test_create_recept_invalid_data():
    invalid_recept_data = {
        "name": "Recipe 1",
        "count_view": "invalid_count_view",
        "cooking_time": 60,
        "descriptions": "Lorem ipsum",
        "ingredients_list": [{"name": "Ingredient 1"}, {"name": "Ingredient 2"}],
    }
    response = client.post("/recept", json=invalid_recept_data)
    assert response.status_code == 422


test_get_all_recepts()
test_get_recept_by_id()
test_get_recept_by_invalid_id()
test_create_recept()
test_create_recept_invalid_data()
test_number()
