from http import HTTPStatus

import pytest

from goals.models import Goal


@pytest.mark.django_db
def test_delete_by_owner(client, logged_in_user, goal_for_category):
    goal = goal_for_category
    url = f"/goals/goal/{goal.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = Goal.objects.get(id=goal.id)
    assert category_is_deleted.is_deleted is True


@pytest.mark.django_db
def test_delete_forbidden_to_unauthorized_user(client, goal_for_category_user2):
    goal = goal_for_category_user2
    url = f"/goals/goal/{goal.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_forbidden_to_user_wo_rights(
    client, logged_in_user, goal_for_category_user2
):
    goal = goal_for_category_user2
    url = f"/goals/goal/{goal.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_forbidden_to_reader(
    client, logged_in_user, goal_for_category_user2_user1_reader
):
    goal = goal_for_category_user2_user1_reader
    url = f"/goals/goal/{goal.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_allowed_to_writer(
    client, logged_in_user, goal_for_category_user2_user1_writer
):
    goal = goal_for_category_user2_user1_writer
    url = f"/goals/goal/{goal.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = Goal.objects.get(id=goal.id)
    assert category_is_deleted.is_deleted is True
