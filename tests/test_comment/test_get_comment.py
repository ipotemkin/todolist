from http import HTTPStatus

import pytest

from goals.serializers import CommentSerializer

URL = "/goals/goal_comment/{}"


@pytest.mark.django_db
def test_one_by_owner(
        client,
        logged_in_user,
        comment
):
    expected_response = CommentSerializer(comment).data

    response = client.get(URL.format(comment.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        comment_for_goal_user2
):
    comment = comment_for_goal_user2
    response = client.get(URL.format(comment.id))

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_one_forbidden_to_unauthorized_user(
        client,
        comment_for_goal_user2
):
    comment = comment_for_goal_user2
    response = client.get(URL.format(comment.id))

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_one_allowed_to_reader(
        client,
        logged_in_user,
        comment_for_goal_user2_user1_reader
):
    comment = comment_for_goal_user2_user1_reader
    expected_response = CommentSerializer(comment).data

    response = client.get(URL.format(comment.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_allowed_to_writer(
        client,
        logged_in_user,
        comment_for_goal_user2_user1_writer
):
    comment = comment_for_goal_user2_user1_writer
    expected_response = CommentSerializer(comment).data

    response = client.get(URL.format(comment.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_not_found(client, logged_in_user):
    response = client.get(URL.format(1000))

    assert response.status_code == HTTPStatus.NOT_FOUND
