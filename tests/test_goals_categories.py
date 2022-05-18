from http import HTTPStatus

import pytest

from goals.models import GoalCategory, Board, BoardParticipant

from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_goal_category_get_all_by_owner(
            client,
            logged_in_user,
            categories_and_board
    ):
    category_1, category_2, _ = categories_and_board

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_all_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        categories_and_board_user2
):
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.django_db
def test_goal_category_get_all_forbidden_to_unauthorized_user(
        client,
        user2,
        categories_and_board_user2
):
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_get_all_allowed_to_reader(
        client,
        logged_in_user,
        user2,
        categories_and_board_user2_user1_reader
):
    category_1, category_2, _ = categories_and_board_user2_user1_reader

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_all_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        categories_and_board_user2_user1_writer
):
    category_1, category_2, _ = categories_and_board_user2_user1_writer

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get("/goals/goal_category/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_one_by_owner(
        client,
        logged_in_user,
        category_and_board
):
    category, board = category_and_board
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_one_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        category_and_board_user2
):
    category, _ = category_and_board_user2

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_goal_category_get_one_forbidden_to_unauthorized_user(
        client,
        user2,
        category_and_board_user2
):
    category, _ = category_and_board_user2

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_get_one_allowed_to_reader(
        client,
        logged_in_user,
        user2,
        category_and_board_user2_user1_reader
):
    category, board = category_and_board_user2_user1_reader
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_one_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        category_and_board_user2_user1_writer
):
    category, board = category_and_board_user2_user1_writer
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_not_found(client, logged_in_user):
    response = client.get("/goals/goal_category/1000")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_goal_category_not_found_for_user_wo_rights(
        client,
        logged_in_user,
        user2,
        category_and_board_user2
):
    category, board = category_and_board_user2
    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


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
        category_and_board_user2
):
    _, board = category_and_board_user2
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
        category_and_board_user2
):
    _, board = category_and_board_user2
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
        category_and_board_user2_user1_reader
):
    _, board = category_and_board_user2_user1_reader
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
        category_and_board_user2_user1_writer
):
    _, board = category_and_board_user2_user1_writer
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


@pytest.mark.django_db
def test_goal_category_partial_update_by_owner(client, logged_in_user, category_and_board):
    category, board = category_and_board
    new_category_title = "New testing category"
    data = {"title": new_category_title}
    expected_response = GoalCategorySerializer(category).data
    expected_response["title"] = new_category_title

    response = client.patch(
        f"/goals/goal_category/{category.id}",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop("updated")
    expected_response.pop("updated")

    assert response_json == expected_response


@pytest.mark.django_db
def test_goal_category_partial_update_forbidden_to_unauthorized_user(
        client,
        user2,
        category_and_board_user2
):
    category, board = category_and_board_user2
    new_category_title = "New testing category"
    data = {"title": new_category_title}

    response = client.patch(
        f"/goals/goal_category/{category.id}",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_partial_update_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        category_and_board_user2
):
    category, board = category_and_board_user2
    new_category_title = "New testing category"
    data = {"title": new_category_title}

    response = client.patch(
        f"/goals/goal_category/{category.id}",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_goal_category_partial_update_forbidden_to_reader(
        client,
        logged_in_user,
        user2,
        category_and_board_user2_user1_reader
):
    category, board = category_and_board_user2_user1_reader
    new_category_title = "New testing category"
    data = {"title": new_category_title}

    response = client.patch(
        f"/goals/goal_category/{category.id}",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_partial_update_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        category_and_board_user2_user1_writer
):
    category, board = category_and_board_user2_user1_writer
    new_category_title = "New testing category"
    data = {"title": new_category_title}
    expected_response = GoalCategorySerializer(category).data
    expected_response["title"] = new_category_title

    response = client.patch(
        f"/goals/goal_category/{category.id}",
        data,
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop("updated")
    expected_response.pop("updated")

    assert response_json == expected_response


@pytest.mark.django_db
def test_goal_category_delete_by_owner(
        client,
        logged_in_user,
        category_and_board
):
    category, board = category_and_board
    url = f"/goals/goal_category/{category.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = GoalCategory.objects.get(id=category.id)
    assert category_is_deleted.is_deleted is True


@pytest.mark.django_db
def test_goal_category_delete_forbidden_to_unauthorized_user(
        client,
        user2,
        category_and_board_user2
):
    category, board = category_and_board_user2
    url = f"/goals/goal_category/{category.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_delete_forbidden_to_user_wo_rights(
        client,
        logged_in_user,
        user2,
        category_and_board_user2
):
    category, board = category_and_board_user2
    url = f"/goals/goal_category/{category.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_goal_category_delete_forbidden_to_reader(
        client,
        logged_in_user,
        user2,
        category_and_board_user2_user1_reader
):
    category, board = category_and_board_user2_user1_reader
    url = f"/goals/goal_category/{category.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_goal_category_delete_allowed_to_writer(
        client,
        logged_in_user,
        user2,
        category_and_board_user2_user1_writer
):
    category, board = category_and_board_user2_user1_writer
    url = f"/goals/goal_category/{category.id}"

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = GoalCategory.objects.get(id=category.id)
    assert category_is_deleted.is_deleted is True
