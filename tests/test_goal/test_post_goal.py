from http import HTTPStatus

import pytest

GOAL_NAME = "New goal name"
DUE_DATE = "2022-07-01"


@pytest.mark.django_db
def test_create_by_owner(client, logged_in_user, category_for_user1):
    data = {
        "title": GOAL_NAME,
        "category": category_for_user1.id,
        "due_date": DUE_DATE
    }

    response = client.post(
        f"/goals/goal/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_create_forbidden_to_unauthorized_user(
        client,
        category_for_user1,
):
    data = {
        "title": GOAL_NAME,
        "category": category_for_user1.id,
        "due_date": DUE_DATE
    }

    response = client.post(
        f"/goals/goal/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_create_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        category_for_user2
):
    data = {
        "title": GOAL_NAME,
        "category": category_for_user2.id,
        "due_date": DUE_DATE
    }

    response = client.post(
        f"/goals/goal/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_create_forbidden_to_reader(
        client,
        logged_in_user,
        category_for_board_user2_user1_reader
):
    data = {
        "title": GOAL_NAME,
        "category": category_for_board_user2_user1_reader.id,
        "due_date": DUE_DATE
    }

    response = client.post(
        f"/goals/goal/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_create_allowed_to_writer(
        client,
        logged_in_user,
        category_for_board_user2_user1_writer
):
    data = {
        "title": GOAL_NAME,
        "category": category_for_board_user2_user1_writer.id,
        "due_date": DUE_DATE
    }

    response = client.post(
        f"/goals/goal/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CREATED
