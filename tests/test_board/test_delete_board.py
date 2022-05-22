from http import HTTPStatus

import pytest

from goals.models import Board

URL = "/goals/board/{}"


@pytest.mark.django_db
def test_delete_by_owner(client, logged_in_user, board, boardparticipant_user1_owner):
    url = URL.format(board.id)

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    board_deleted = Board.objects.get(id=board.id)
    assert board_deleted.is_deleted is True


@pytest.mark.django_db
def test_delete_forbidden_to_unauthorized_user(
    client, board, boardparticipant_user1_owner
):
    url = URL.format(board.id)
    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_forbidden_to_user_wo_rights(
    client, logged_in_user, board, boardparticipant_user2_owner
):
    response = client.delete(URL.format(board.id))
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_forbidden_to_reader(
    client, logged_in_user, board, boardparticipant_user1_reader
):
    response = client.delete(URL.format(board.id))
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_forbidden_to_writer(
    client, logged_in_user, board, boardparticipant_user1_writer
):
    response = client.delete(URL.format(board.id))
    assert response.status_code == HTTPStatus.FORBIDDEN
