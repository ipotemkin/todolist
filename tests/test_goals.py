import pytest

from core.models import User
from goals.models import GoalCategory, Board, BoardParticipant
from tests.factory import GoalCategoryFactory

from goals.serializers import GoalCategorySerializer

new_ad_base = {
    "name": "Testing advertisement",
    "price": 1000,
}

new_ad_ext = {
    "is_published": False,
    "description": None,
    "image": None,
    "id": 1
}

new_ad = {**new_ad_base, **new_ad_ext}


# @pytest.mark.django_db
def test_healthcheck(client):
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


@pytest.mark.django_db
def test_goal_category_get_all(client, logged_in_user):
    # goal_categories = GoalCategoryFactory.create_batch(2)
    board = Board.objects.create(title="Testing board")
    user = User.objects.get(username="james")
    goal_category_1 = GoalCategory.objects.create(title="Testing category", user=user, board=board)
    BoardParticipant.objects.create(board=board, user=user)
    goal_category_2 = GoalCategory.objects.create(title="Testing category 2", user=user, board=board)

    # expected_category_list_response = {
    #     "count": 2,
    #     "next": None,
    #     "previous": None,
    #     "results": GoalCategorySerializer(goal_categories, many=True).data
    # }
    expected_response = [
        GoalCategorySerializer(goal_category_1).data,
        GoalCategorySerializer(goal_category_2).data,
    ]
    response = client.get("/goals/goal_category/list")
    assert response.status_code == 200
    # assert response.data == expected_category_list_response
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_get_one(client, logged_in_user, category_and_board):
    category, board = category_and_board
    expected_response = GoalCategorySerializer(category).data
    response = client.get(f"/goals/goal_category/{category.id}")
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.django_db
def test_goal_category_partial_update(client, logged_in_user, category_and_board):
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
    assert response.status_code == 200

    response_json = response.json()
    response_json.pop("updated")
    expected_response.pop("updated")
    assert response_json == expected_response


# @pytest.mark.django_db
# def test_ad_get_one(client, user_token, ad):
#     token, _ = user_token
#     response = client.get(
#         "/ads/3/",
#         HTTP_AUTHORIZATION="Bearer " + token
#     )
#     new_ad["author"] = ad.author_id
#     new_ad["category"] = ad.category_id
#     new_ad["id"] = ad.id
#
#     assert response.status_code == 200
#     assert response.data == new_ad


# @pytest.mark.django_db
# def test_ad_create(client, ad):
#     data = dict(
#         **new_ad_base,
#         author=ad.author_id,
#         category=ad.category_id
#     )
#     response = client.post(
#         "/ads/",
#         data,
#         content_type="application/json"
#     )
#
#     new_ad["author"] = ad.author_id
#     new_ad["category"] = ad.category_id
#     new_ad["id"] = ad.author_id
#
#     assert response.status_code == 201
#     assert response.data == new_ad
#
#
# @pytest.mark.django_db
# def test_ad_update(client, ad, admin_user_token):
#     token, _ = admin_user_token
#     data = dict(price=2000)
#     response = client.patch(
#         f"/ads/{ad.id}/",
#         data,
#         content_type="application/json",
#         HTTP_AUTHORIZATION="Bearer " + token
#     )
#
#     new_ad["author"] = ad.author_id
#     new_ad["category"] = ad.category_id
#     new_ad["id"] = ad.author_id
#     new_ad["price"] = 2000
#
#     assert response.status_code == 200
#     assert response.data == new_ad
#
#
# @pytest.mark.django_db
# def test_ad_delete(client, ad, admin_user_token):
#     token, _ = admin_user_token
#     response = client.delete(
#         f"/ads/{ad.id}/",
#         content_type="application/json",
#         HTTP_AUTHORIZATION="Bearer " + token
#     )
#
#     assert response.status_code == 204
#     assert response.data is None
