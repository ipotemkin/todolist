from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_healthcheck(client):
    response = client.get("/health/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}
