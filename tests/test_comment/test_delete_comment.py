from http import HTTPStatus

import pytest


URL = "/goals/goal_comment/{}"


@pytest.mark.django_db
def test_delete_by_owner(client, logged_in_user, comment):
    url = URL.format(comment.id)

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_forbidden_to_unauthorized_user(client, comment):
    url = URL.format(comment.id)
    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_forbidden_to_user_wo_rights(
    client, logged_in_user, comment_for_goal_user2
):
    comment = comment_for_goal_user2
    response = client.delete(URL.format(comment.id))
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_forbidden_to_reader(
    client, logged_in_user, comment_for_goal_user2_user1_reader
):
    comment = comment_for_goal_user2_user1_reader
    response = client.delete(URL.format(comment.id))
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_allowed_to_writer(
    client, logged_in_user, comment_for_goal_user2_user1_writer
):
    comment = comment_for_goal_user2_user1_writer
    url = URL.format(comment.id)

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_forbidden_to_not_owner_but_reader(
    client, logged_in_user, comment_user2_for_goal_user2_user1_reader
):
    comment = comment_user2_for_goal_user2_user1_reader
    url = URL.format(comment.id)

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_forbidden_to_not_owner_but_writer(
    client, logged_in_user, comment_user2_for_goal_user2_user1_writer
):
    comment = comment_user2_for_goal_user2_user1_writer
    url = URL.format(comment.id)
    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN
