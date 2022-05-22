from http import HTTPStatus

import pytest

from goals.serializers import BoardListSerializer

URL = "/goals/board/list"


@pytest.mark.django_db
def test_get_all_by_owner(
    client,
    logged_in_user,
    board,
    board2,
    boardparticipant_user1_owner,
    boardparticipant_board2_user1_owner,
):
    expected_response = [
        BoardListSerializer(board).data,
        BoardListSerializer(board2).data,
    ]
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_forbidden_to_user_wo_rights(
    client,
    logged_in_user2,
    board,
    board2,
    boardparticipant_user1_owner,
    boardparticipant_board2_user1_owner,
):
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.django_db
def test_get_all_forbidden_to_unauthorized_user(
    client,
    board,
    board2,
    boardparticipant_user1_owner,
    boardparticipant_board2_user1_owner,
):
    response = client.get(URL)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_all_allowed_to_reader(
    client,
    logged_in_user,
    board,
    board2,
    boardparticipant_user1_reader,
    boardparticipant_board2_user1_reader,
):
    expected_response = [
        BoardListSerializer(board).data,
        BoardListSerializer(board2).data,
    ]
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_allowed_to_writer(
    client,
    logged_in_user,
    board,
    board2,
    boardparticipant_user1_writer,
    boardparticipant_board2_user1_writer,
):
    expected_response = [
        BoardListSerializer(board).data,
        BoardListSerializer(board2).data,
    ]
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response
