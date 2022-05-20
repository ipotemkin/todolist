from http import HTTPStatus

import pytest

BOARD_NAME = "New board"
URL = "/goals/board/create"

DATA = {"title": BOARD_NAME}


@pytest.mark.django_db
def test_create_by_owner(client, logged_in_user):
    response = client.post(
        URL,
        DATA,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_create_forbidden_to_unauthorized_user(client):
    response = client.post(
        URL,
        DATA,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
