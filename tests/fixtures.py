import pytest

from goals.models import Board, BoardParticipant, GoalCategory, Goal, Comment

TEST_USERNAME = "james"
TEST_USERNAME_2 = "user2"
USER_PASSWORD = "qwerty123"
CATEGORY_NAME = "Testing category name"
CATEGORY_NAME_2 = "Testing category name 2"
GOAL_NAME = "Testing goal name"
GOAL_NAME_2 = "Testing goal name 2"
DUE_DATE = "2022-07-01"
COMMENT_TEXT = "Testing comment"
COMMENT_TEXT_2 = "Testing comment 2"


# @pytest.fixture(scope="session")
# def initial_test_data(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         # Wrap in try + atomic block to do non crashing rollback
#         try:
#             with transaction.atomic():
#                 yield
#                 raise Exception
#         except Exception:
#             pass
#
#
# @pytest.fixture(scope="session", autouse=True)
# def some_initial_data(initial_test_data):
#     User.objects.create_user(
#         username=TEST_USERNAME, password=USER_PASSWORD
#     )
#     # Data added here will stay in db for the whole test session


@pytest.fixture
@pytest.mark.django_db
def user1(django_user_model):
    return django_user_model.objects.create_user(
        username=TEST_USERNAME, password=USER_PASSWORD
    )


@pytest.fixture
# @pytest.mark.django_db
def user2(django_user_model):
    return django_user_model.objects.create_user(
        username=TEST_USERNAME_2, password=USER_PASSWORD
    )


@pytest.fixture
# @pytest.mark.django_db
def logged_in_user(client, user1):
    client.login(username=user1.username, password=USER_PASSWORD)
    return user1


@pytest.fixture
# @pytest.mark.django_db
def logged_in_user2(client, user2):
    client.login(username=TEST_USERNAME_2, password=USER_PASSWORD)
    return user2


@pytest.fixture
# @pytest.mark.django_db
def board():
    board_name = "Testing board name"
    # return Board.objects.create(title=board_name)
    board = Board.objects.create(title=board_name)
    print(board)
    return board


@pytest.fixture
# @pytest.mark.django_db
def board2():
    board_name = "Testing board name 2"
    return Board.objects.create(title=board_name)


@pytest.fixture
# @pytest.mark.django_db
def category_for_user1(user1, board, boardparticipant_user1_owner):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture
# @pytest.mark.django_db
def goal_for_category(category_for_user1):
    return Goal.objects.create(
        title=GOAL_NAME, category=category_for_user1, due_date=DUE_DATE
    )


@pytest.fixture
# @pytest.mark.django_db
def goal_for_category_user2(category_for_user2):
    return Goal.objects.create(
        title=GOAL_NAME, category=category_for_user2, due_date=DUE_DATE
    )


@pytest.fixture
# @pytest.mark.django_db
def goal_for_category_user2_user1_reader(category_for_board_user2_user1_reader):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_board_user2_user1_reader,
        due_date=DUE_DATE,
    )


@pytest.fixture
# @pytest.mark.django_db
def goal_for_category_user2_user1_writer(category_for_board_user2_user1_writer):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_board_user2_user1_writer,
        due_date=DUE_DATE,
    )


def make_categories(user, board):
    category = GoalCategory.objects.create(title=CATEGORY_NAME, user=user, board=board)
    category_2 = GoalCategory.objects.create(
        title=CATEGORY_NAME_2, user=user, board=board
    )
    return category, category_2


def make_goals(category):
    goal = Goal.objects.create(title=GOAL_NAME, category=category, due_date=DUE_DATE)
    goal_2 = Goal.objects.create(
        title=GOAL_NAME_2, category=category, due_date=DUE_DATE
    )
    return goal, goal_2


def make_comments(goal, user):
    comment = Comment.objects.create(text=COMMENT_TEXT, goal=goal, user=user)
    comment_2 = Comment.objects.create(text=COMMENT_TEXT_2, goal=goal, user=user)
    return comment, comment_2


@pytest.fixture
@pytest.mark.django_db
def goals_for_category(category_for_user1):
    return make_goals(category_for_user1)


@pytest.fixture
@pytest.mark.django_db
def goals_for_category_user2(category_for_user2):
    return make_goals(category_for_user2)


@pytest.fixture
@pytest.mark.django_db
def goals_for_category_user2_user1_reader(category_for_board_user2_user1_reader):
    return make_goals(category_for_board_user2_user1_reader)


@pytest.fixture
@pytest.mark.django_db
def goals_for_category_user2_user1_writer(category_for_board_user2_user1_writer):
    return make_goals(category_for_board_user2_user1_writer)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user1(user1, board, boardparticipant_user1_owner):
    return make_categories(user1, board)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user2(user2, board, boardparticipant_user2_owner):
    return make_categories(user2, board)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user2_user1_reader(
    user1, board, boardparticipant_user2_owner, boardparticipant_user1_reader
):
    return make_categories(user1, board)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user2_user1_writer(
    user1, board, boardparticipant_user1_writer, boardparticipant_user2_owner
):
    return make_categories(user1, board)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user1_owner(board, user1):
    return BoardParticipant.objects.create(board=board, user=user1)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_board2_user1_owner(board2, user1):
    return BoardParticipant.objects.create(board=board2, user=user1)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user2_owner(board, user2):
    return BoardParticipant.objects.create(board=board, user=user2)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user1_reader(board, user1):
    return BoardParticipant.objects.create(
        board=board, user=user1, role=BoardParticipant.Role.reader
    )


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_board2_user1_reader(board2, user1):
    return BoardParticipant.objects.create(
        board=board2, user=user1, role=BoardParticipant.Role.reader
    )


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user1_writer(board, user1):
    return BoardParticipant.objects.create(
        board=board, user=user1, role=BoardParticipant.Role.writer
    )


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_board2_user1_writer(board2, user1):
    return BoardParticipant.objects.create(
        board=board2, user=user1, role=BoardParticipant.Role.writer
    )


@pytest.fixture
@pytest.mark.django_db
def category_for_user2(board, user2, boardparticipant_user2_owner):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user2, board=board)


@pytest.fixture
@pytest.mark.django_db
def category_for_board_user2_user1_reader(
    board, user1, user2, boardparticipant_user1_reader
):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture
@pytest.mark.django_db
def category_for_board_user2_user1_writer(
    board, user1, user2, boardparticipant_user1_writer
):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture
@pytest.mark.django_db
def comment(user1, goal_for_category):
    return Comment.objects.create(text=COMMENT_TEXT, goal=goal_for_category, user=user1)


@pytest.fixture
@pytest.mark.django_db
def comment_for_goal_user2(user1, goal_for_category_user2):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2, user=user1
    )


@pytest.fixture
@pytest.mark.django_db
def comment_for_goal_user2_user1_reader(user1, goal_for_category_user2_user1_reader):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_reader, user=user1
    )


@pytest.fixture
@pytest.mark.django_db
def comment_user2_for_goal_user2_user1_reader(
    user2, goal_for_category_user2_user1_reader
):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_reader, user=user2
    )


@pytest.fixture
@pytest.mark.django_db
def comment_user2_for_goal_user2_user1_writer(
    user2, goal_for_category_user2_user1_writer
):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_writer, user=user2
    )


@pytest.fixture
@pytest.mark.django_db
def comment_for_goal_user2_user1_writer(user1, goal_for_category_user2_user1_writer):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_writer, user=user1
    )


@pytest.fixture
@pytest.mark.django_db
def comments(user1, goal_for_category):
    return make_comments(goal_for_category, user1)


@pytest.fixture
@pytest.mark.django_db
def comments_for_goal_user2(user2, goal_for_category_user2):
    return make_comments(goal_for_category_user2, user2)


@pytest.fixture
@pytest.mark.django_db
def comments_for_goal_user2_user1_reader(user2, goal_for_category_user2_user1_reader):
    return make_comments(goal_for_category_user2_user1_reader, user2)


@pytest.fixture
@pytest.mark.django_db
def comments_for_goal_user2_user1_writer(user2, goal_for_category_user2_user1_writer):
    return make_comments(goal_for_category_user2_user1_writer, user2)
