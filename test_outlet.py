import requests
from fastapi import status
import pytest
from config import url, api_key


@pytest.mark.skip(reason="This test is used as a helper test for other test functions.")
def test_food_outlet_details(outlet):
    assert type(outlet["id"]) is int
    assert type(outlet["name"]) is str

    assert (outlet["location"] is None) or (type(outlet["location"]) is dict)
    if outlet["location"] is not None:
        assert type(outlet["location"]["latitude"]) is str
        assert type(outlet["location"]["longitude"]) is str

    assert (outlet["landmark"] is None) or (type(outlet["landmark"]) is str)
    assert (outlet["open_time"] is None) or (type(outlet["open_time"]) is str)
    assert (outlet["close_time"] is None) or (type(outlet["close_time"]) is str)

    assert (outlet["rating"] is None) or (type(outlet["rating"]) is dict)
    if outlet["rating"] is not None:
        assert type(outlet["rating"]["total"]) is float
        assert type(outlet["rating"]["count"]) is int

    assert (outlet["menu"] == None) or (type(outlet["menu"]) is list)
    if outlet["menu"] is not None:
        for item in outlet["menu"]:
            assert type(item["name"]) is str
            assert type(item["price"]) is int
            assert (item["description"] == None) or (type(item["description"]) is str)

            assert (item["rating"] == None) or (type(item["rating"]) is dict)
            if item["rating"] is not None:
                assert type(item["rating"]["total"]) is float
                assert type(item["rating"]["count"]) is int

            assert (item["size"] == None) or (type(item["size"]) is str)
            assert (item["cal"] == None) or (type(item["cal"]) is int)
            assert (item["image"] == None) or (type(item["image"]) is str)

    assert (outlet["image"] == None) or (type(outlet["image"]) is str)


@pytest.mark.skip(reason="This test is used as a helper test for other test functions.")
def test_item_details(item):
    assert type(item["id"]) is int
    assert type(item["name"]) is str
    assert type(item["price"]) is int
    assert (item["description"] == None) or (type(item["description"]) is str)

    assert (item["rating"] == None) or (type(item["rating"]) is dict)
    if item["rating"] is not None:
        assert type(item["rating"]["total"]) is float
        assert type(item["rating"]["count"]) is int

    assert (item["size"] == None) or (type(item["size"]) is str)
    assert (item["cal"] == None) or (type(item["cal"]) is int)
    assert (item["image"] == None) or (type(item["image"]) is str)

    assert type(item["outlet_id"]) is int


def test_get_all_food_outlet_details_success():
    response = requests.get(f"{url}/food-outlet", headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["outlets"]) is list

    outlets = response.json()["outlets"]

    for outlet in outlets:
        test_food_outlet_details(outlet)


def test_get_all_food_outlet_details_error_noApiKey():
    response = requests.get(f"{url}/food-outlet")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_get_all_food_outlet_details_error_invalidApiKey():
    response = requests.get(f"{url}/food-outlet", headers={"x-api-key": "abc123"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


def test_get_food_outlet_details_success():
    response = requests.get(f"{url}/food-outlet/2", headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["outlet"]) is dict

    outlet = response.json()["outlet"]
    test_food_outlet_details(outlet)


def test_get_food_outlet_details_error_notFound():
    response = requests.get(f"{url}/food-outlet/999999", headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Food outlet not found"}


def test_get_food_outlet_details_error_noApiKey():
    response = requests.get(f"{url}/food-outlet/1")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_get_food_outlet_details_error_invalidApiKey():
    response = requests.get(f"{url}/food-outlet/1", headers={"x-api-key": "abc123"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


def test_search_food_outlets_success():
    response = requests.request(
        method="GET",
        url=f"{url}/search/food-outlet",
        json={"name": "r"},
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["outlets"]) is list

    for outlet in response.json()["outlets"]:
        test_food_outlet_details(outlet)


def test_search_food_outlets_error_notFound():
    response = requests.request(
        method="GET",
        url=f"{url}/search/food-outlet",
        json={"name": "abcdefghijklmnopqrstuvwxz"},
        headers={"x-api-key": api_key},
    )

    print(response.json())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "No food outlets found"}


def test_search_food_outlets_error_noApiKey():
    response = requests.get(f"{url}/search/food-outlet", data={"name": "r"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_search_food_outlets_error_invalidApiKey():
    response = requests.get(
        f"{url}/search/food-outlet", json={"name": "r"}, headers={"x-api-key": "abc123"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


id: int | None = None


def test_create_food_outlet_success():
    outlet = None

    response = requests.request(
        method="POST",
        url=f"{url}/food-outlet",
        json={"name": "sea post - test outlet"},
        headers={"x-api-key": api_key},
    )

    print(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert type(response.json()["outlet"]) is dict

    outlet = response.json()["outlet"]

    global id
    id = outlet["id"]
    assert type(id) is int
    assert outlet["name"] == "sea post - test outlet"

    for key, value in outlet.items():
        assert value is None if key not in ["id", "name"] else True


def test_create_food_outlet_error_outletExists():
    response = requests.request(
        method="POST",
        url=f"{url}/food-outlet",
        json={"name": "Atul Bakery"},
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Food outlet already exists"}


def test_create_food_outlet_error_noApiKey():
    response = requests.post(
        f"{url}/food-outlet", data={"name": "sea post - test outlet"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_create_food_outlet_error_invalidApiKey():
    response = requests.post(
        f"{url}/food-outlet",
        json={"name": "sea post - test outlet"},
        headers={"x-api-key": "abc123"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


new_id: int | None = None


def test_update_food_outlet_success():
    global id
    response = requests.request(
        method="PUT",
        url=f"{url}/food-outlet/{id}",
        json={"name": "test outlet"},
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()["outlet"]) is dict

    outlet = response.json()["outlet"]

    global new_id
    new_id = outlet["id"]
    assert new_id == id

    assert outlet["name"] == "test outlet"
    for key, value in outlet.items():
        assert value is None if key not in ["id", "name"] else True


def test_update_food_outlet_error_outletNotFound():
    response = requests.request(
        method="PUT",
        url=f"{url}/food-outlet/9999999",
        json={"name": "test outlet"},
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Food outlet not found"}


def test_update_food_outlet_error_noApiKey():
    response = requests.put(
        f"{url}/food-outlet/1", data={"name": "sea post - test outlet"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_update_food_outlet_error_invalidApiKey():
    response = requests.put(
        f"{url}/food-outlet/1",
        json={"name": "sea post - test outlet"},
        headers={"x-api-key": "abc123"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


def test_delete_food_outlet_success():
    global id
    response = requests.request(
        method="DELETE",
        url=f"{url}/food-outlet/{id}",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_food_outlet_error_outletNotFound():
    response = requests.request(
        method="DELETE",
        url=f"{url}/food-outlet/9999999",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Food outlet not found"}


def test_delete_food_outlet_error_noApiKey():
    response = requests.delete(f"{url}/food-outlet/1")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_delete_food_outlet_error_invalidApiKey():
    response = requests.delete(
        f"{url}/food-outlet/1",
        headers={"x-api-key": "abc123"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


item_id = None
item = None


def test_add_menu_item_success():
    global item_id, item
    item = {
        "name": "test item",
        "price": 25,
        "description": None,
        "rating": None,
        "size": None,
        "cal": None,
        "image": None,
    }

    response = requests.request(
        method="POST",
        url=f"{url}/food-outlet/1/menu/food-item",
        json=item,
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_201_CREATED

    item = response.json()["item"]

    assert type(item) is dict
    item_id = item["id"]
    test_item_details(item)


def test_add_menu_item_error_itemExists():
    item = {
        "name": "aloo paratha",
        "price": 40,
        "description": None,
        "rating": None,
        "size": None,
        "cal": None,
        "image": None,
    }
    response = requests.request(
        method="POST",
        url=f"{url}/food-outlet/2/menu/food-item",
        json=item,
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Menu item already exists"}


def test_add_menu_item_error_outletNotFound():
    item = {
        "name": "test item",
        "price": 25,
        "description": None,
        "rating": None,
        "size": None,
        "cal": None,
        "image": None,
    }

    response = requests.request(
        method="POST",
        url=f"{url}/food-outlet/9999999/menu/food-item",
        json=item,
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Food outlet not found"}


def test_add_menu_item_error_noApiKey():
    item = {
        "name": "test item",
        "price": 25,
        "description": None,
        "rating": None,
        "size": None,
        "cal": None,
        "image": None,
    }

    response = requests.request(
        method="POST", url=f"{url}/food-outlet/1/menu/food-item", json=item
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_add_menu_item_error_invalidApiKey():
    item = {
        "name": "test item",
        "price": 25,
        "description": None,
        "rating": None,
        "size": None,
        "cal": None,
        "image": None,
    }

    response = requests.request(
        method="POST",
        url=f"{url}/food-outlet/1/menu/food-item",
        json=item,
        headers={"x-api-key": "abc123"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


def test_update_menu_item_success():
    global item, item_id
    item["price"] = 30
    item["description"] = "this is a test item"
    response = requests.request(
        method="PUT",
        url=f"{url}/food-outlet/1/menu/food-item/{item_id}",
        json=item,
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_200_OK
    item = response.json()["item"]

    assert type(item) is dict
    test_item_details(item)


def test_update_menu_item_error_itemNotFound():
    invalid_item = {
        "name": "invalid test item",
        "price": 30,
        "description": "this is an invalid test item",
        "rating": None,
        "size": None,
        "cal": None,
        "image": None,
    }
    response = requests.request(
        method="PUT",
        url=f"{url}/food-outlet/1/menu/food-item/99999999",
        json=invalid_item,
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Menu item not found"}


def test_update_menu_item_error_outletNotFound():
    global item, item_id

    response = requests.request(
        method="PUT",
        url=f"{url}/food-outlet/99999999/menu/food-item/{item_id}",
        json=item,
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Food outlet not found"}


def test_update_menu_item_error_noApiKey():
    global item, item_id
    response = requests.request(
        method="PUT", url=f"{url}/food-outlet/1/menu/food-item/{item_id}", json=item
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_update_menu_item_error_invalidApiKey():
    global item, item_id
    response = requests.request(
        method="PUT",
        url=f"{url}/food-outlet/1/menu/food-item/{item_id}",
        json=item,
        headers={"x-api-key": "abc123"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}


def test_delete_menu_item_success():
    global item_id

    response = requests.request(
        method="DELETE",
        url=f"{url}/food-outlet/1/menu/food-item/{item_id}",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_menu_item_error_itemNotFound():
    response = requests.request(
        method="DELETE",
        url=f"{url}/food-outlet/1/menu/food-item/99999999",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Menu item not found"}


def test_delete_menu_item_error_outletNotFound():
    global item_id
    response = requests.request(
        method="DELETE",
        url=f"{url}/food-outlet/999999/menu/food-item/{item_id}",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Food outlet not found"}


def test_delete_menu_item_error_noApiKey():
    global item_id
    response = requests.request(
        method="DELETE",
        url=f"{url}/food-outlet/1/menu/food-item/{item_id}",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_delete_menu_item_error_invalidApiKey():
    global item_id
    response = requests.request(
        method="DELETE",
        url=f"{url}/food-outlet/1/menu/food-item/{item_id}",
        headers={"x-api-key": "abc123"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}
