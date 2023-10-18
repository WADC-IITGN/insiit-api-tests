import requests
from fastapi import status
from config import url, api_key


def test_root_success():
    response = requests.get(f"{url}", headers={"x-api-key": api_key})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "hello world"}


def test_root_error_noApiKey():
    response = requests.get(f"{url}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Missing headers: x-api-key"}


def test_root_error_invalidApiKey():
    response = requests.get(f"{url}", headers={"x-api-key": "invalid"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Could not validate API key"}
