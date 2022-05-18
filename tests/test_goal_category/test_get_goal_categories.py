from http import HTTPStatus

import pytest

from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_goal_category_get_all_by_owner(
        client,
        logged_in_user,
        categories_for_user1
):
    category_1, category_2 = categories_for_user1

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_all_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        categories_for_user2
):
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.django_db
def test_goal_category_get_all_forbidden_to_unauthorized_user(
        client,
        user2,
        categories_for_user2
):
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_get_all_allowed_to_reader(
        client,
        logged_in_user,
        user2,
        categories_for_user2_user1_reader
):
    category_1, category_2 = categories_for_user2_user1_reader

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_all_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        categories_for_user2_user1_writer
):
    category_1, category_2 = categories_for_user2_user1_writer

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response
