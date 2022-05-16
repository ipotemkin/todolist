import os
from enum import Enum, unique, auto
from typing import Optional

from datetime import date

from django.core.management import BaseCommand
from django.db.models import Q
from pydantic import BaseModel

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory, Board, BoardParticipant
from todolist import settings


class NewGoal(BaseModel):
    cat_id: Optional[int] = None
    goal_title: Optional[str] = None
    due_date: Optional[date] = None  # datetime.now()

    def complete(self) -> bool:
        return None not in (self.cat_id, self.goal_title, self.due_date)


@unique
class StateEnum(Enum):
    CHOOSE_CATEGORY = auto()
    CHOSEN_CATEGORY = auto()
    SET_GOAL_TITLE = auto()
    CHOOSE_BOARD = auto()
    CHOSEN_BOARD = auto()
    CHOOSE_GOAL = auto()
    # CHOSEN_GOAL = auto()
    # CREATE_CATEGORY = auto()


class FSMData(BaseModel):
    state: StateEnum
    goal: NewGoal
    board_id: Optional[int] = None


FSM_STATES: dict[int, FSMData] = dict()


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    @staticmethod
    def _gen_verification_code() -> str:
        return os.urandom(12).hex()

    @staticmethod
    def _clean_fsm_states(chat_id: int) -> None:
        if chat_id in FSM_STATES:
            FSM_STATES.pop(chat_id)

    @staticmethod
    def _get_goal_query(tg_user: TgUser, and_: Q = Q()) -> Q:
        return (
            Q(category__board__participants__user_id=tg_user.user_id)
            & Q(is_deleted=False)
            & and_
        )

    @staticmethod
    def _get_category_query(tg_user: TgUser, and_: Q = Q()) -> Q:
        return (
            Q(board__participants__user_id=tg_user.user_id)
            & Q(is_deleted=False)
            & and_
        )

    @staticmethod
    def _get_board_query(tg_user: TgUser, and_: Q = Q()) -> Q:
        return (
            Q(participants__user_id=tg_user.user_id)
            & Q(is_deleted=False)
            & (
                Q(participants__role=BoardParticipant.Role.owner)
                | Q(participants__role=BoardParticipant.Role.writer)
            )
            & and_
        )

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1

                # TODO remove after debugging
                print(item.message)

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
            f'#{goal.id} {goal.title} срок:{goal.due_date} статус: {Goal.Status(goal.status).label}'
            for goal in Goal.objects.filter(self._get_goal_query(tg_user))
        ]

        text = ''
        if (
            tg_user.chat_id in FSM_STATES
            and FSM_STATES[tg_user.chat_id].state == StateEnum.CHOOSE_GOAL
        ):
            text = 'Select goal:\n'

        if resp_goals:
            text += '\n'.join(resp_goals)
        else:
            text = '[no goals found]'
            self._clean_fsm_states(tg_user.chat_id)

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=text
        )

    def handle_create_goal(self, msg: Message, tg_user: TgUser):
        FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.CHOOSE_CATEGORY, goal=NewGoal())
        self.handle_category_list(msg=msg, tg_user=tg_user)

    def handle_category_list(self, msg: Message, tg_user: TgUser):
        resp_categories: list[str] = [
            f'#{category.id} {category.title}'
            for category in GoalCategory.objects.filter(self._get_category_query(tg_user))
        ]

        text = ''
        if (
            tg_user.chat_id in FSM_STATES
            and FSM_STATES[tg_user.chat_id].state == StateEnum.CHOOSE_CATEGORY
        ):
            text = 'Select category:\n'

        if resp_categories:
            text += '\n'.join(resp_categories)
        else:
            text = '[no categories found]'
            self._clean_fsm_states(tg_user.chat_id)

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=text
        )

    def handle_board_list(self, msg: Message, tg_user: TgUser):
        resp_boards: list[str] = [
            f'#{board.id} {board.title}'
            for board in Board.objects.filter(self._get_board_query(tg_user))
        ]

        text = ''
        if (
            tg_user.chat_id in FSM_STATES
            and FSM_STATES[tg_user.chat_id].state == StateEnum.CHOOSE_BOARD
        ):
            text = 'Select board:\n'

        if resp_boards:
            text += '\n'.join(resp_boards)
        else:
            text = '[no boards found]'
            self._clean_fsm_states(tg_user.chat_id)

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=text
        )

    def handle_create_category(self, msg: Message, tg_user: TgUser):
        FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.CHOOSE_BOARD, goal=NewGoal())
        self.handle_board_list(msg=msg, tg_user=tg_user)

    def handle_save_selected_category(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            cat_id = int(msg.text)
            if GoalCategory.objects.filter(
                self._get_category_query(tg_user, and_=Q(id=cat_id))
            ).count():
                FSM_STATES[tg_user.chat_id].goal.cat_id = cat_id
                self.tg_client.send_message(chat_id=msg.chat.id, text='[set title]')
                FSM_STATES[tg_user.chat_id].state = StateEnum.CHOSEN_CATEGORY
                return

        self.tg_client.send_message(chat_id=msg.chat.id, text='[invalid category id]')

    def handle_save_selected_board(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            board_id = int(msg.text)
            if Board.objects.filter(self._get_board_query(tg_user, and_=Q(id=board_id))).count():
                FSM_STATES[tg_user.chat_id].board_id = board_id
                self.tg_client.send_message(chat_id=msg.chat.id, text='[set title for a category]')
                FSM_STATES[tg_user.chat_id].state = StateEnum.CHOSEN_BOARD
                return

        self.tg_client.send_message(chat_id=msg.chat.id, text='[invalid board id]')

    def handle_set_goal_title(self, msg: Message, tg_user: TgUser):
        FSM_STATES[tg_user.chat_id].goal.goal_title = msg.text
        self.tg_client.send_message(chat_id=msg.chat.id, text='[set due_date]')
        FSM_STATES[tg_user.chat_id].state = StateEnum.SET_GOAL_TITLE

    def handle_save_new_goal(self, msg: Message, tg_user: TgUser):
        goal: NewGoal = FSM_STATES[tg_user.chat_id].goal
        goal.due_date = msg.text
        if goal.complete():
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.cat_id,
                due_date=goal.due_date,
            )
            self.tg_client.send_message(chat_id=msg.chat.id, text='[new goal created]')
        else:
            self.tg_client.send_message(chat_id=msg.chat.id, text='[something went wrong]')

        self._clean_fsm_states(tg_user.chat_id)

    def handle_save_new_category(self, msg: Message, tg_user: TgUser):
        category = msg.text
        GoalCategory.objects.create(
            title=category,
            user_id=tg_user.user_id,
            board_id=FSM_STATES[tg_user.chat_id].board_id
        )
        self.tg_client.send_message(chat_id=msg.chat.id, text='[new category created]')
        self._clean_fsm_states(tg_user.chat_id)

    def handle_delete_goal(self, msg: Message, tg_user: TgUser):
        FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.CHOOSE_GOAL, goal=NewGoal())
        self.handle_goal_list(msg=msg, tg_user=tg_user)

    def handle_delete_selected_goal(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            goal_id = int(msg.text)
            goal = Goal.objects.filter(self._get_goal_query(tg_user, and_=Q(id=goal_id))).first()
            if goal:
                goal.is_deleted = True
                goal.save(update_fields=['is_deleted'])
                self.tg_client.send_message(chat_id=msg.chat.id, text='[goal has been deleted]')
                self._clean_fsm_states(tg_user.chat_id)
                return

        self.tg_client.send_message(chat_id=msg.chat.id, text='[invalid goal id]')

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if msg.text == '/goals':
            self.handle_goal_list(msg=msg, tg_user=tg_user)

        elif msg.text == '/cats':
            self.handle_category_list(msg=msg, tg_user=tg_user)

        elif msg.text == '/boards':
            self.handle_board_list(msg=msg, tg_user=tg_user)

        elif msg.text == '/create_goal':
            self.handle_create_goal(msg=msg, tg_user=tg_user)

        elif msg.text == '/create_cat':
            self.handle_create_category(msg=msg, tg_user=tg_user)

        elif msg.text == '/delete_goal':
            self.handle_delete_goal(msg=msg, tg_user=tg_user)

        elif msg.text == '/cancel':
            self._clean_fsm_states(tg_user.chat_id)

        elif tg_user.chat_id in FSM_STATES:
            state: StateEnum = FSM_STATES[tg_user.chat_id].state

            if state == StateEnum.CHOOSE_CATEGORY:
                self.handle_save_selected_category(msg=msg, tg_user=tg_user)

            elif state == StateEnum.CHOSEN_CATEGORY:
                self.handle_set_goal_title(msg=msg, tg_user=tg_user)

            elif state == StateEnum.SET_GOAL_TITLE:
                self.handle_save_new_goal(msg=msg, tg_user=tg_user)

            if state == StateEnum.CHOOSE_BOARD:
                self.handle_save_selected_board(msg=msg, tg_user=tg_user)

            if state == StateEnum.CHOSEN_BOARD:
                self.handle_save_new_category(msg=msg, tg_user=tg_user)

            if state == StateEnum.CHOOSE_GOAL:
                self.handle_delete_selected_goal(msg=msg, tg_user=tg_user)

        elif msg.text.startswith('/'):
            self.tg_client.send_message(chat_id=msg.chat.id, text='[unknown command]')

        # TODO remove after debugging
        print(FSM_STATES)

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
