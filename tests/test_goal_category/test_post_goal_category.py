from http import HTTPStatus

import pytest

from goals.models import Board, BoardParticipant


@pytest.mark.django_db
def test_goal_category_create_by_owner(client, logged_in_user):
    category_name = "Testing category name"
    board_name = "Testing board name"
    board = Board.objects.create(title=board_name)
    BoardParticipant.objects.create(board=board, user=logged_in_user)

    data = {
        "title": category_name,
        "board": board.id
    }

    response = client.post(
        f"/goals/goal_category/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_goal_category_create_forbidden_to_unauthorized_user(
        client,
        user2,
        board,
):
    category_name = "Testing category name"

    data = {
        "title": category_name,
        "board": board.id
    }

    response = client.post(
        f"/goals/goal_category/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_create_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        board,
):
    category_name = "Testing category name"

    data = {
        "title": category_name,
        "board": board.id
    }

    response = client.post(
        f"/goals/goal_category/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_create_forbidden_to_reader(
        client,
        logged_in_user,
        user2,
        board,
        category_for_board_user2_user1_reader
):
    category_name = "Testing category name"

    data = {
        "title": category_name,
        "board": board.id
    }

    response = client.post(
        f"/goals/goal_category/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_create_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        board,
        category_for_board_user2_user1_writer
):
    category_name = "Testing category name"

    data = {
        "title": category_name,
        "board": board.id
    }

    response = client.post(
        f"/goals/goal_category/create",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CREATED
