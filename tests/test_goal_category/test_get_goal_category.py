from http import HTTPStatus

import pytest

from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_goal_category_get_one_by_owner(
        client,
        logged_in_user,
        category_for_user1
):
    category = category_for_user1
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_one_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        category_for_user2
):
    category = category_for_user2

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_goal_category_get_one_forbidden_to_unauthorized_user(
        client,
        category_for_user2
):
    category = category_for_user2

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_get_one_allowed_to_reader(
        client,
        logged_in_user,
        category_for_board_user2_user1_reader
):
    category = category_for_board_user2_user1_reader
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_one_allowed_to_writer(
        client,
        logged_in_user,
        category_for_board_user2_user1_writer
):
    category = category_for_board_user2_user1_writer
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_not_found(client, logged_in_user):
    response = client.get("/goals/goal_category/1000")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_goal_category_not_found_for_user_wo_rights(
        client,
        logged_in_user,
        user2,
        category_for_user2
):
    category = category_for_user2
    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.NOT_FOUND
