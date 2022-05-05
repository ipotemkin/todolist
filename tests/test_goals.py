import pytest

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
# def test_root(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {'status': 'ok'}


@pytest.mark.django_db
def test_goal_category_get_all(client):
    goal_categories = GoalCategoryFactory.create_batch(2)
    expected_ad_list_response = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": GoalCategorySerializer(goal_categories, many=True).data
    }

    response = client.get("/goals/goal_category/list")
    assert response.status_code == 200
    # assert response.data == expected_ad_list_response


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
