from http import HTTPStatus

import pytest

from goals.serializers import GoalSerializer


NEW_GOAL_NAME = 'New goal name'


def get_patch_response(client, goal):
    return client.patch(
        f'/goals/goal/{goal.id}',
        {'title': NEW_GOAL_NAME},
        content_type='application/json'
    )


@pytest.mark.django_db
def test_partial_update_by_owner(client, logged_in_user, goal_for_category):
    goal = goal_for_category

    expected_response = GoalSerializer(goal).data
    expected_response['title'] = NEW_GOAL_NAME

    response = get_patch_response(client, goal)

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop('updated')
    expected_response.pop('updated')

    assert response_json == expected_response


@pytest.mark.django_db
def test_partial_update_forbidden_to_unauthorized_user(
        client,
        goal_for_category
):
    goal = goal_for_category

    expected_response = GoalSerializer(goal).data
    expected_response['title'] = NEW_GOAL_NAME

    response = get_patch_response(client, goal)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_update_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        goal_for_category_user2
):
    response = get_patch_response(client, goal_for_category_user2)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_partial_update_forbidden_to_reader(
        client,
        logged_in_user,
        goal_for_category_user2_user1_reader
):
    response = get_patch_response(client, goal_for_category_user2_user1_reader)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_update_allowed_to_writer(
        client,
        logged_in_user,
        goal_for_category_user2_user1_writer
):
    goal = goal_for_category_user2_user1_writer
    response = get_patch_response(client, goal)

    expected_response = GoalSerializer(goal).data
    expected_response['title'] = NEW_GOAL_NAME

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop('updated')
    expected_response.pop('updated')

    assert response_json == expected_response
