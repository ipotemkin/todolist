import os
from enum import Enum, unique, auto
from typing import Optional

from django.core.management import BaseCommand
from pydantic import BaseModel

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from todolist import settings


class NewGoal(BaseModel):
    cat_id: Optional[int] = None
    goal_title: Optional[str] = None

    def complete(self) -> bool:
        return None not in (self.cat_id, self.goal_title)


@unique
class StateEnum(Enum):
    CREATE_CATEGORY = auto()
    CHOSEN_CATEGORY = auto()


class FSMData:
    state: StateEnum
    goal: NewGoal


FSM_STATES: dict[int, FSMData] = dict()


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    @staticmethod
    def _gen_verification_code() -> str:
        return os.urandom(12).hex()

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                # self.tg_client.send_message(chat_id=item.message.chat.id, text=item.message.text)
                self.handle_message(item.message)

    def handle_user_wo_verification(self, msg: Message, tg_user: TgUser):
        code: str = self._gen_verification_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'[verification code] {code}'
        )

    def handle_goal_list(self, msg: Message, tg_user: TgUser):
        resp_goals: list[str] = [
            f'#{goal.id} {goal.title} срок:{goal.due_date}'
            for goal in Goal.objects.filter(
                category__board__participants__user_id=tg_user.user_id,
                is_deleted=False
            )
        ]
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text='\n'.join(resp_goals) or '[no goals found]'
        )

    def handle_category_list(self, msg: Message, tg_user: TgUser):
        resp_categories: list[str] = [
            f'#{category.id} {category.title}'
            for category in GoalCategory.objects.filter(
                board__participants__user_id=tg_user.user_id,
                is_deleted=False
            )
        ]
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text='\n'.join(resp_categories) or '[no categories found]'
        )

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if msg.text == '/goals':
            self.handle_goal_list(msg=msg, tg_user=tg_user)
        elif msg.text == '/create_goal':
            self.handle_category_list(msg=msg, tg_user=tg_user)

        elif msg.text == '/categories':
            self.handle_category_list(msg=msg, tg_user=tg_user)
        elif msg.text.startswith('/'):
            self.tg_client.send_message(chat_id=msg.chat.id, text='[unknown command]')

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=msg.chat.id,
            defaults={
                'username': msg.from_.username
            }
        )
        if created:
            self.tg_client.send_message(chat_id=msg.chat.id, text='[hello]')
        elif not tg_user.user:
            self.handle_user_wo_verification(msg=msg, tg_user=tg_user)
        else:
            self.handle_verified_user(msg=msg, tg_user=tg_user)

        # if TgUser.objects.filter(chat_id=msg.chat.id).exists():
        #     self.tg_client.send_message(chat_id=msg.chat.id, text='[exists]')
        # else:
        #     self.tg_client.send_message(chat_id=msg.chat.id, text='[hello]')


