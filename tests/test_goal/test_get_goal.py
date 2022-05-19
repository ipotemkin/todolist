from http import HTTPStatus

import pytest

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_one_by_owner(
        client,
        logged_in_user,
        goal_for_category
):
    goal = goal_for_category
    expected_response = GoalSerializer(goal).data

    response = client.get(f"/goals/goal/{goal.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        goal_for_category_user2
):
    goal = goal_for_category_user2
    response = client.get(f"/goals/goal_category/{goal.id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_get_one_forbidden_to_unauthorized_user(
        client,
        goal_for_category_user2
):
    goal = goal_for_category_user2
    response = client.get(f"/goals/goal_category/{goal.id}")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_one_allowed_to_reader(
        client,
        logged_in_user,
        goal_for_category_user2_user1_reader
):
    goal = goal_for_category_user2_user1_reader
    expected_response = GoalSerializer(goal).data

    response = client.get(f"/goals/goal/{goal.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_allowed_to_writer(
        client,
        logged_in_user,
        goal_for_category_user2_user1_writer
):
    goal = goal_for_category_user2_user1_writer
    expected_response = GoalSerializer(goal).data

    response = client.get(f"/goals/goal/{goal.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_not_found(client, logged_in_user):
    response = client.get("/goals/goal/1000")

    assert response.status_code == HTTPStatus.NOT_FOUND
