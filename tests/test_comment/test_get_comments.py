from http import HTTPStatus

import pytest

from goals.serializers import CommentSerializer

URL = "/goals/goal_comment/list"


@pytest.mark.django_db
def test_get_all_by_owner(
        client,
        logged_in_user,
        comments
):
    comment_1, comment_2 = comments

    expected_response = [
        CommentSerializer(comment_2).data,
        CommentSerializer(comment_1).data,
    ]
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        goals_for_category_user2
):
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.django_db
def test_get_all_forbidden_to_unauthorized_user(
        client,
        comments
):
    response = client.get(URL)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_all_allowed_to_reader(
        client,
        logged_in_user,
        comments_for_goal_user2_user1_reader
):
    comment_1, comment_2 = comments_for_goal_user2_user1_reader

    expected_response = [
        CommentSerializer(comment_2).data,
        CommentSerializer(comment_1).data,
    ]
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_allowed_to_writer(
        client,
        logged_in_user,
        comments_for_goal_user2_user1_writer
):
    comment_1, comment_2 = comments_for_goal_user2_user1_writer

    expected_response = [
        CommentSerializer(comment_2).data,
        CommentSerializer(comment_1).data,
    ]
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response
