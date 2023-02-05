import pytest


@pytest.mark.django_db
def test_ad_create(client, access_token, user, category):
    data = {
        "name": "test test test",
        "category": category.name,
        "author": user.username,
        "price": 100,
        "description": "test"
    }

    expected_data = {
        "id": 1,
        "is_published": False,
        "author": user.username,
        "category": category.name,
        "name": "test test test",
        "price": 100,
        "description": "test",
        "image": None
    }

    response = client.post('/ad/', data, HTTP_AUTHORIZATION='Bearer ' + access_token)

    assert response.status_code == 201
    assert response.data == expected_data
