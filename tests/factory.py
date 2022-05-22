import factory.django

from core.models import User
from goals.models import GoalCategory, Board


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    # password = "qwerty123"

    # username = "james"
    password = 'qwerty123'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = 'Test board name'


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = 'Testing category'
    # user = User.objects.create_user(username="james", password="qwerty123")
    user_id = 1
    # user = factory.SubFactory(UserFactory)
    # user_id = User.objects.filter(username="james").first().id
    board = factory.SubFactory(BoardFactory)
    # is_deleted = False


# class CatFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Cat
#
#     name = "Testing category"
#
#
# class AdFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Ad
#
#     name = "Testing advertisement"
#     price = 1000
#     author = factory.SubFactory(UserFactory)
#     category = factory.SubFactory(CatFactory)


# class SelectionFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Selection
#
#     name = "Testing selection"
#     owner = factory.SubFactory(UserFactory)
#     items = [1]
