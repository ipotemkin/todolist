import pytest

# from ads import models
from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory

TEST_USERNAME = "james"
TEST_USERNAME_2 = "user2"


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user(client, django_user_model):
    username = TEST_USERNAME
    password = "qwerty123"

    django_user_model.objects.create_user(
        username=username,
        password=password
    )
    client.login(username=username, password=password)

    return User.objects.get(username=username)


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user2(client, django_user_model):
    username = TEST_USERNAME_2
    password = "qwerty123"

    django_user_model.objects.create_user(
        username=username,
        password=password
    )
    client.login(username=username, password=password)
    return User.objects.get(username=username)


@pytest.fixture()
@pytest.mark.django_db
def user2(client, django_user_model):
    username = TEST_USERNAME_2
    password = "qwerty123"

    user2 = django_user_model.objects.create_user(
        username=username,
        password=password
    )
    return user2


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


@pytest.fixture()
@pytest.mark.django_db
def categories_and_board(client):
    category_name = "Testing category"
    category_2_name = "Testing category 2"
    board_name = "Testing board"
    board = Board.objects.create(title=board_name)
    user = User.objects.get(username=TEST_USERNAME)
    BoardParticipant.objects.create(board=board, user=user)
    category = GoalCategory.objects.create(title=category_name, user=user, board=board)
    category_2 = GoalCategory.objects.create(title=category_2_name, user=user, board=board)

    return category, category_2, board


@pytest.fixture()
@pytest.mark.django_db
def categories_and_board_user2(client):
    category_name = "Testing category"
    category_2_name = "Testing category 2"
    board_name = "Testing board"
    board = Board.objects.create(title=board_name)
    user = User.objects.get(username=TEST_USERNAME_2)
    BoardParticipant.objects.create(board=board, user=user)
    category = GoalCategory.objects.create(title=category_name, user=user, board=board)
    category_2 = GoalCategory.objects.create(title=category_2_name, user=user, board=board)

    return category, category_2, board


@pytest.fixture()
@pytest.mark.django_db
def categories_and_board_user2_user1_reader(client):
    category_name = "Testing category"
    category_2_name = "Testing category 2"
    board_name = "Testing board"
    board = Board.objects.create(title=board_name)

    user2 = User.objects.get(username=TEST_USERNAME_2)
    BoardParticipant.objects.create(board=board, user=user2, role=BoardParticipant.Role.reader)

    user1 = User.objects.get(username=TEST_USERNAME)
    BoardParticipant.objects.create(board=board, user=user1)

    category = GoalCategory.objects.create(title=category_name, user=user1, board=board)
    category_2 = GoalCategory.objects.create(title=category_2_name, user=user1, board=board)

    return category, category_2, board


@pytest.fixture()
@pytest.mark.django_db
def categories_and_board_user2_user1_writer(client):
    category_name = "Testing category"
    category_2_name = "Testing category 2"
    board_name = "Testing board"
    board = Board.objects.create(title=board_name)

    user2 = User.objects.get(username=TEST_USERNAME_2)
    BoardParticipant.objects.create(board=board, user=user2, role=BoardParticipant.Role.writer)

    user1 = User.objects.get(username=TEST_USERNAME)
    BoardParticipant.objects.create(board=board, user=user1)

    category = GoalCategory.objects.create(title=category_name, user=user1, board=board)
    category_2 = GoalCategory.objects.create(title=category_2_name, user=user1, board=board)

    return category, category_2, board


@pytest.fixture()
@pytest.mark.django_db
def category_and_board_user2(client):
    category_name = "Testing category name"
    board_name = "Testing board name"
    board = Board.objects.create(title=board_name)
    user = User.objects.get(username=TEST_USERNAME_2)
    BoardParticipant.objects.create(board=board, user=user)
    category = GoalCategory.objects.create(title=category_name, user=user, board=board)

    return category, board


@pytest.fixture()
@pytest.mark.django_db
def category_and_board_user2_user1_reader(client):
    category_name = "Testing category name"
    board_name = "Testing board name"
    board = Board.objects.create(title=board_name)
    user2 = User.objects.get(username=TEST_USERNAME_2)
    user = User.objects.get(username=TEST_USERNAME)

    BoardParticipant.objects.create(board=board, user=user2)
    BoardParticipant.objects.create(board=board, user=user, role=BoardParticipant.Role.reader)
    category = GoalCategory.objects.create(title=category_name, user=user, board=board)

    return category, board


@pytest.fixture()
@pytest.mark.django_db
def category_and_board_user2_user1_writer(client):
    category_name = "Testing category name"
    board_name = "Testing board name"
    board = Board.objects.create(title=board_name)
    user2 = User.objects.get(username=TEST_USERNAME_2)
    user = User.objects.get(username=TEST_USERNAME)

    BoardParticipant.objects.create(board=board, user=user2)
    BoardParticipant.objects.create(board=board, user=user, role=BoardParticipant.Role.writer)
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
