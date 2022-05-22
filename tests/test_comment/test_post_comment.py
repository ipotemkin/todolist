from http import HTTPStatus

import pytest

COMMENT_TEXT = "New comment"
URL = "/goals/goal_comment/create"


@pytest.mark.django_db
def test_create_by_owner(client, logged_in_user, goal_for_category):
    data = {
        "text": COMMENT_TEXT,
        "goal": goal_for_category.id,
        "user": logged_in_user.id,
    }

    response = client.post(URL, data, content_type="application/json")

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_create_forbidden_to_unauthorized_user(
    client,
    user1,
    goal_for_category,
):
    data = {"text": COMMENT_TEXT, "goal": goal_for_category.id, "user": user1.id}

    response = client.post(URL, data, content_type="application/json")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_create_forbidden_to_user_wo_rights(
    client, logged_in_user, goal_for_category_user2
):
    data = {
        "text": COMMENT_TEXT,
        "goal": goal_for_category_user2.id,
        "user": logged_in_user.id,
    }

    response = client.post(URL, data, content_type="application/json")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_create_forbidden_to_reader(
    client, logged_in_user, goal_for_category_user2_user1_reader
):
    data = {
        "text": COMMENT_TEXT,
        "goal": goal_for_category_user2_user1_reader.id,
        "user": logged_in_user.id,
    }

    response = client.post(URL, data, content_type="application/json")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_create_allowed_to_writer(
    client, logged_in_user, goal_for_category_user2_user1_writer
):
    data = {
        "text": COMMENT_TEXT,
        "goal": goal_for_category_user2_user1_writer.id,
        "user": logged_in_user.id,
    }

    response = client.post(URL, data, content_type="application/json")

    assert response.status_code == HTTPStatus.CREATED
