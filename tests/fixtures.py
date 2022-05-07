import pytest

# from ads import models
from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory

TEST_USERNAME = "james"


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user(client, django_user_model):
    username = TEST_USERNAME
    password = "qwerty123"

    django_user_model.objects.create_user(
        username=username,
        password=password
    )
    logged_in = client.login(username=username, password=password)

    return logged_in


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user2(client, django_user_model):
    username = "user2"
    password = "qwerty123"

    django_user_model.objects.create_user(
        username=username,
        password=password
    )
    logged_in = client.login(username=username, password=password)
    return logged_in


@pytest.fixture()
@pytest.mark.django_db
def category_and_board(client):
    category_name = "Testing category name"
    board_name = "Testing board name"
    board = Board.objects.create(title=board_name)
    user = User.objects.get(username=TEST_USERNAME)
    BoardParticipant.objects.create(board=board, user=user)
    category = GoalCategory.objects.create(title=category_name, user=user, board=board)

    return category, board


# @pytest.fixture()
# @pytest.mark.django_db
# def category_and_board_user2(client):
#     category_name = "Testing category name user 2"
#     board_name = "Testing board name 2"
#     board = Board.objects.create(title=board_name)
#     user = User.objects.get(username=TEST_USERNAME)
#     BoardParticipant.objects.create(board=board, user=user)
#     category = GoalCategory.objects.create(title=category_name, user=user, board=board)
#
#     return category, board

    # response = client.post(
    #     "/users/token/",
    #     {"username": username, "password": password},
    #     format="json"
    # )
    #
    # return response.data["access"], user.id


# @pytest.fixture()
# @pytest.mark.django_db
# def admin_user_token(client, django_user_model):
#     username = "james"
#     password = "james"
#
#     user = django_user_model.objects.create_user(
#         username=username,
#         password=password,
#         role=models.User.ADMIN,
#     )
#
#     response = client.post(
#         "/users/token/",
#         {"username": username, "password": password},
#         format="json"
#     )
#
#     return response.data["access"], user.id
