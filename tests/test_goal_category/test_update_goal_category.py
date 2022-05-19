from http import HTTPStatus

import pytest

from goals.serializers import GoalCategorySerializer


NEW_CATEGORY_NAME = "New category name"


def get_patch_response(client, category):
    return client.patch(
        f"/goals/goal_category/{category.id}",
        {"title": NEW_CATEGORY_NAME},
        content_type="application/json"
    )


@pytest.mark.django_db
def test_partial_update_by_owner(client, logged_in_user, category_for_user1):
    category = category_for_user1

    expected_response = GoalCategorySerializer(category).data
    expected_response["title"] = NEW_CATEGORY_NAME

    response = get_patch_response(client, category)

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop("updated")
    expected_response.pop("updated")

    assert response_json == expected_response


@pytest.mark.django_db
def test_partial_update_forbidden_to_unauthorized_user(
        client,
        user2,
        category_for_user2
):
    category = category_for_user2

    expected_response = GoalCategorySerializer(category).data
    expected_response["title"] = NEW_CATEGORY_NAME

    response = get_patch_response(client, category)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_update_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        category_for_user2
):
    response = get_patch_response(client, category_for_user2)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_partial_update_forbidden_to_reader(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_reader
):
    response = get_patch_response(client, category_for_board_user2_user1_reader)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_update_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_writer
):
    category = category_for_board_user2_user1_writer
    response = get_patch_response(client, category)

    expected_response = GoalCategorySerializer(category).data
    expected_response["title"] = NEW_CATEGORY_NAME

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop("updated")
    expected_response.pop("updated")

    assert response_json == expected_response
