from http import HTTPStatus
from freezegun import freeze_time
# from django.utils import timezone

import pytest

from goals.serializers import BoardSerializer

UPDATED_BOARD = "Updated board"


def get_patch_response(client, board):
    return client.patch(
        f"/goals/board/{board.id}",
        {"title": UPDATED_BOARD},
        content_type="application/json"
    )


@pytest.mark.django_db
@freeze_time('1970-01-01T05:00:00', tz_offset=+0)
def test_partial_update_by_owner(
        client,
        logged_in_user,
        board,
        boardparticipant_user1_owner
):
    expected_response = BoardSerializer(board).data
    expected_response["title"] = UPDATED_BOARD
    expected_response["updated"] = '1970-01-01T05:00:00Z'

    response = get_patch_response(client, board)

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    # response_json.pop("updated")
    # expected_response.pop("updated")

    assert response_json == expected_response


@pytest.mark.django_db
def test_partial_update_forbidden_to_unauthorized_user(
        client,
        board,
        boardparticipant_user1_owner
):
    expected_response = BoardSerializer(board).data
    expected_response["title"] = UPDATED_BOARD
    expected_response["updated"] = '1970-01-01T05:00:00Z'

    response = get_patch_response(client, board)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_update_forbidden_to_user_wo_rights(
        client,
        logged_in_user2,
        board,
        boardparticipant_user1_owner
):
    expected_response = BoardSerializer(board).data
    expected_response["title"] = UPDATED_BOARD
    expected_response["updated"] = '1970-01-01T05:00:00Z'

    response = get_patch_response(client, board)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_partial_update_forbidden_to_reader(
        client,
        logged_in_user,
        board,
        boardparticipant_user1_reader
):
    expected_response = BoardSerializer(board).data
    expected_response["title"] = UPDATED_BOARD
    expected_response["updated"] = '1970-01-01T05:00:00Z'

    response = get_patch_response(client, board)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_update_allowed_to_writer(
        client,
        board,
        boardparticipant_user1_writer
):
    expected_response = BoardSerializer(board).data
    expected_response["title"] = UPDATED_BOARD
    expected_response["updated"] = '1970-01-01T05:00:00Z'

    response = get_patch_response(client, board)

    assert response.status_code == HTTPStatus.FORBIDDEN
