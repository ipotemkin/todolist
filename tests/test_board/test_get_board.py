from http import HTTPStatus

import pytest

from goals.serializers import BoardSerializer


@pytest.mark.django_db
class TestGetBoard:
    url = "/goals/board/{}"

    def test_one_by_owner(
        self, client, logged_in_user, board, boardparticipant_user1_owner
    ):
        expected_response = BoardSerializer(board).data

        response = client.get(self.url.format(board.id))

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_response

    def test_get_one_forbidden_to_user_wo_rights(
        self, client, logged_in_user2, board, boardparticipant_user1_owner
    ):
        response = client.get(self.url.format(board.id))

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_one_forbidden_to_unauthorized_user(
        self, client, board, boardparticipant_user1_owner
    ):
        response = client.get(self.url.format(board.id))

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_get_one_allowed_to_reader(
        self, client, logged_in_user, board, boardparticipant_user1_reader
    ):
        expected_response = BoardSerializer(board).data

        response = client.get(self.url.format(board.id))

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_response

    def test_get_one_allowed_to_writer(
        self, client, logged_in_user, board, boardparticipant_user1_writer
    ):
        expected_response = BoardSerializer(board).data

        response = client.get(self.url.format(board.id))

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_response

    def test_not_found(self, client, logged_in_user):
        response = client.get(self.url.format(1000))

        assert response.status_code == HTTPStatus.NOT_FOUND
