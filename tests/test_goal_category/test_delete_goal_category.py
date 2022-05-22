from http import HTTPStatus

import pytest

from goals.models import GoalCategory


@pytest.mark.django_db
def test_delete_by_owner(
        client,
        logged_in_user,
        category_for_user1
):
    category = category_for_user1
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = GoalCategory.objects.get(id=category.id)
    assert category_is_deleted.is_deleted is True


@pytest.mark.django_db
def test_delete_forbidden_to_unauthorized_user(
        client,
        user2,
        category_for_user2
):
    category = category_for_user2
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        category_for_user2
):
    category = category_for_user2
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_forbidden_to_reader(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_reader
):
    category = category_for_board_user2_user1_reader
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_writer
):
    category = category_for_board_user2_user1_writer
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = GoalCategory.objects.get(id=category.id)
    assert category_is_deleted.is_deleted is True
