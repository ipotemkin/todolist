import pytest

from goals.models import Board, BoardParticipant, GoalCategory, Goal

TEST_USERNAME = "james"
TEST_USERNAME_2 = "user2"
USER_PASSWORD = "qwerty123"
CATEGORY_NAME = "Testing category name"
CATEGORY_NAME_2 = "Testing category name 2"
GOAL_NAME = "Testing goal name"
GOAL_NAME_2 = "Testing goal name 2"
DUE_DATE = "2022-07-01"


@pytest.fixture()
@pytest.mark.django_db
def user1(client, django_user_model):
    return django_user_model.objects.create_user(
        username=TEST_USERNAME,
        password=USER_PASSWORD
    )


@pytest.fixture()
@pytest.mark.django_db
def user2(client, django_user_model):
    return django_user_model.objects.create_user(
        username=TEST_USERNAME_2,
        password=USER_PASSWORD
    )


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user(client, user1):
    client.login(username=user1.username, password=USER_PASSWORD)
    return user1


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user2(client, user2):
    client.login(username=TEST_USERNAME_2, password=USER_PASSWORD)
    return user2


@pytest.fixture()
@pytest.mark.django_db
def board(client):
    board_name = "Testing board name"
    return Board.objects.create(title=board_name)


@pytest.fixture()
@pytest.mark.django_db
def category_for_user1(client, user1, board, boardparticipant_user1_owner):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture()
@pytest.mark.django_db
def goal_for_category(client, category_for_user1):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_user1,
        due_date=DUE_DATE
    )


@pytest.fixture()
@pytest.mark.django_db
def goal_for_category_user2(client, category_for_user2):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_user2,
        due_date=DUE_DATE
    )


@pytest.fixture()
@pytest.mark.django_db
def goal_for_category_user2_user1_reader(
        client,
        category_for_board_user2_user1_reader
):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_board_user2_user1_reader,
        due_date=DUE_DATE
    )


@pytest.fixture()
@pytest.mark.django_db
def goal_for_category_user2_user1_writer(
        client,
        category_for_board_user2_user1_writer
):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_board_user2_user1_writer,
        due_date=DUE_DATE
    )



def make_categories(user, board):
    category = GoalCategory.objects.create(title=CATEGORY_NAME, user=user, board=board)
    category_2 = GoalCategory.objects.create(title=CATEGORY_NAME_2, user=user, board=board)
    return category, category_2


def make_goals(category):
    goal = Goal.objects.create(title=GOAL_NAME, category=category, due_date=DUE_DATE)
    goal_2 = Goal.objects.create(title=GOAL_NAME_2, category=category, due_date=DUE_DATE)
    return goal, goal_2


@pytest.fixture()
@pytest.mark.django_db
def goals_for_category(client, category_for_user1):
    return make_goals(category_for_user1)


@pytest.fixture()
@pytest.mark.django_db
def goals_for_category_user2(client, category_for_user2):
    return make_goals(category_for_user2)


@pytest.fixture()
@pytest.mark.django_db
def goals_for_category_user2_user1_reader(client, category_for_board_user2_user1_reader):
    return make_goals(category_for_board_user2_user1_reader)


@pytest.fixture()
@pytest.mark.django_db
def goals_for_category_user2_user1_writer(client, category_for_board_user2_user1_writer):
    return make_goals(category_for_board_user2_user1_writer)


@pytest.fixture()
@pytest.mark.django_db
def categories_for_user1(client, user1, board, boardparticipant_user1_owner):
    return make_categories(user1, board)


@pytest.fixture()
@pytest.mark.django_db
def categories_for_user2(client, user2, board, boardparticipant_user2_owner):
    return make_categories(user2, board)


@pytest.fixture()
@pytest.mark.django_db
def categories_for_user2_user1_reader(
        client, user1, board, boardparticipant_user2_owner, boardparticipant_user1_reader
):
    return make_categories(user1, board)


@pytest.fixture()
@pytest.mark.django_db
def categories_for_user2_user1_writer(
        client, user1, board, boardparticipant_user1_writer, boardparticipant_user2_owner
):
    return make_categories(user1, board)


@pytest.fixture()
@pytest.mark.django_db
def boardparticipant_user1_owner(client, board, user1):
    return BoardParticipant.objects.create(board=board, user=user1)


@pytest.fixture()
@pytest.mark.django_db
def boardparticipant_user2_owner(client, board, user2):
    return BoardParticipant.objects.create(board=board, user=user2)


@pytest.fixture()
@pytest.mark.django_db
def boardparticipant_user1_reader(client, board, user1):
    return BoardParticipant.objects.create(
        board=board, user=user1, role=BoardParticipant.Role.reader
    )


@pytest.fixture()
@pytest.mark.django_db
def boardparticipant_user1_writer(client, board, user1):
    return BoardParticipant.objects.create(
        board=board, user=user1, role=BoardParticipant.Role.writer
    )


@pytest.fixture()
@pytest.mark.django_db
def category_for_user2(client, board, user2, boardparticipant_user2_owner):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user2, board=board)


@pytest.fixture()
@pytest.mark.django_db
def category_for_board_user2_user1_reader(
        client, board, user1, user2, boardparticipant_user1_reader
):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture()
@pytest.mark.django_db
def category_for_board_user2_user1_writer(
        client, board, user1, user2, boardparticipant_user1_writer
):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)
