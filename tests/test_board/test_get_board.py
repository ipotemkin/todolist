from http import HTTPStatus

import pytest

from goals.serializers import BoardSerializer

URL = "/goals/board/{}"


@pytest.mark.django_db
def test_one_by_owner(
        client,
        logged_in_user,
        board,
        boardparticipant_user1_owner
):
    expected_response = BoardSerializer(board).data

    response = client.get(URL.format(board.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_forbidden_to_user_wo_rights(
        client,
        logged_in_user2,
        board,
        boardparticipant_user1_owner
):
    response = client.get(URL.format(board.id))

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_get_one_forbidden_to_unauthorized_user(
        client,
        board,
        boardparticipant_user1_owner
):
    response = client.get(URL.format(board.id))

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_one_allowed_to_reader(
        client,
        logged_in_user,
        board,
        boardparticipant_user1_reader
):
    expected_response = BoardSerializer(board).data

    response = client.get(URL.format(board.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_allowed_to_writer(
        client,
        logged_in_user,
        board,
        boardparticipant_user1_writer
):
    expected_response = BoardSerializer(board).data

    response = client.get(URL.format(board.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_not_found(client, logged_in_user):
    response = client.get(URL.format(1000))

    assert response.status_code == HTTPStatus.NOT_FOUND
