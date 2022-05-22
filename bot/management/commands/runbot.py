import re

from django.core.cache import cache

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
    CHOOSE_GOAL_TO_DONE = auto()
    # CHOSEN_GOAL = auto()
    # CREATE_CATEGORY = auto()


class FSMData(BaseModel):
    state: StateEnum
    goal: NewGoal
    board_id: Optional[int] = None


StatusSymbol = {
    Goal.Status.to_do: "▶",
    Goal.Status.in_progress: "⏳",
    Goal.Status.done: "✅",
    Goal.Status.archived: "❎",
}


def set_fsm_state(chat_id: int, fsm: FSMData, timeout=None):
    cache.set(chat_id, fsm.json(), timeout=timeout)


def get_fsm_state(chat_id: int) -> Optional[FSMData]:
    resp = cache.get(chat_id)
    if resp:
        return FSMData.parse_raw(resp)
    return None


def update_tsm_state(chat_id: int, fsm: FSMData) -> bool:
    if cache.get(chat_id):
        del_fsm_state(chat_id)

    if not set_fsm_state(chat_id, fsm):
        return False

    return True


def del_fsm_state(chat_id: int) -> bool:
    return cache.delete(chat_id)


def str2date(s: str) -> Optional[date]:
    match = re.match(r"^([0-9]{4})[.\-/ ]{0,1}([0-9]{2})[.\-/ ]{0,1}([0-9]{2})$", s)
    if not match:
        return None

    try:
        res = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None

    return res


OWNER_WRITER = Q(participants__role=BoardParticipant.Role.owner) | Q(
    participants__role=BoardParticipant.Role.writer
)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    @staticmethod
    def _gen_verification_code() -> str:
        return os.urandom(12).hex()

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
            Q(board__participants__user_id=tg_user.user_id) & Q(is_deleted=False) & and_
        )

    @staticmethod
    def _get_board_query(tg_user: TgUser, and_: Q = Q()) -> Q:
        return Q(participants__user_id=tg_user.user_id) & Q(is_deleted=False) & and_

    def _smth_wrong(self, chat_id) -> None:
        self.tg_client.send_message(chat_id=chat_id, text="[something went wrong]")

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
        cache.set(code, tg_user.username, timeout=60 * 3)

        self.tg_client.send_message(
            chat_id=msg.chat.id, text=f"[verification code] {code}"
        )

    def handle_goal_list(self, msg: Message, tg_user: TgUser):
        resp_goals: list[str] = [
            f"#{goal.id} {goal.title} | 🕒 {goal.due_date} | {StatusSymbol[Goal.Status(goal.status)]}"
            for goal in Goal.objects.filter(self._get_goal_query(tg_user))
        ]

        text = ""
        fsm_state = get_fsm_state(tg_user.chat_id)
        if fsm_state and fsm_state.state in (
            StateEnum.CHOOSE_GOAL,
            StateEnum.CHOOSE_GOAL_TO_DONE,
        ):
            text = "Select goal:\n"

        if resp_goals:
            text += "\n".join(resp_goals)
        else:
            text = "[no goals found]"
            del_fsm_state(tg_user.chat_id)

        self.tg_client.send_message(chat_id=msg.chat.id, text=text)

    def handle_create_goal(self, msg: Message, tg_user: TgUser):
        set_fsm_state(
            tg_user.chat_id, FSMData(state=StateEnum.CHOOSE_CATEGORY, goal=NewGoal())
        )
        self.handle_category_list(msg=msg, tg_user=tg_user)

    def handle_category_list(self, msg: Message, tg_user: TgUser):
        resp_categories: list[str] = [
            f"#{category.id} {category.title}"
            for category in GoalCategory.objects.filter(
                self._get_category_query(tg_user)
            )
        ]

        text = ""
        fsm_state = get_fsm_state(tg_user.chat_id)
        if fsm_state and fsm_state.state == StateEnum.CHOOSE_CATEGORY:
            text = "Select category:\n"

        if resp_categories:
            text += "\n".join(resp_categories)
        else:
            text = "[no categories found]"
            del_fsm_state(tg_user.chat_id)

        self.tg_client.send_message(chat_id=msg.chat.id, text=text)

    def handle_board_list(self, msg: Message, tg_user: TgUser):
        extra_condition = Q()
        text = ""
        fsm_state = get_fsm_state(tg_user.chat_id)
        if fsm_state and fsm_state.state == StateEnum.CHOOSE_BOARD:
            text = "Select board:\n"
            extra_condition = OWNER_WRITER

        resp_boards: list[str] = [
            f"#{board.id} {board.title}"
            for board in Board.objects.filter(
                self._get_board_query(tg_user, and_=extra_condition)
            )
        ]

        if resp_boards:
            text += "\n".join(resp_boards)
        else:
            text = "[no boards found]"
            del_fsm_state(tg_user.chat_id)

        self.tg_client.send_message(chat_id=msg.chat.id, text=text)

    def handle_create_category(self, msg: Message, tg_user: TgUser):
        set_fsm_state(
            tg_user.chat_id, FSMData(state=StateEnum.CHOOSE_BOARD, goal=NewGoal())
        )
        self.handle_board_list(msg=msg, tg_user=tg_user)

    def handle_save_selected_category(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            cat_id = int(msg.text)
            if GoalCategory.objects.filter(
                self._get_category_query(tg_user, and_=Q(id=cat_id))
            ).count():
                fsm_state = get_fsm_state(tg_user.chat_id)
                if fsm_state:
                    fsm_state.goal.cat_id = cat_id
                    fsm_state.state = StateEnum.CHOSEN_CATEGORY
                    update_tsm_state(tg_user.chat_id, fsm_state)
                    self.tg_client.send_message(chat_id=msg.chat.id, text="[set title]")
                    return
                self._smth_wrong(msg.chat.id)
                return

        self.tg_client.send_message(chat_id=msg.chat.id, text="[invalid category id]")

    def handle_save_selected_board(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            board_id = int(msg.text)
            if Board.objects.filter(
                self._get_board_query(tg_user, and_=Q(id=board_id))
            ).count():
                fsm_state = get_fsm_state(tg_user.chat_id)
                if fsm_state:
                    fsm_state.board_id = board_id
                    fsm_state.state = StateEnum.CHOSEN_BOARD
                    update_tsm_state(tg_user.chat_id, fsm_state)
                    self.tg_client.send_message(
                        chat_id=msg.chat.id, text="[set title for a category]"
                    )
                    return
                self._smth_wrong(msg.chat.id)
                return

        self.tg_client.send_message(chat_id=msg.chat.id, text="[invalid board id]")

    def handle_set_goal_title(self, msg: Message, tg_user: TgUser):
        fsm_state = get_fsm_state(tg_user.chat_id)
        if not fsm_state:
            self._smth_wrong(msg.chat.id)
            return
        fsm_state.goal.goal_title = msg.text
        fsm_state.state = StateEnum.SET_GOAL_TITLE
        update_tsm_state(tg_user.chat_id, fsm_state)
        self.tg_client.send_message(chat_id=msg.chat.id, text="[set due_date]")

    def handle_save_new_goal(self, msg: Message, tg_user: TgUser):
        fsm_state = get_fsm_state(tg_user.chat_id)
        if not fsm_state:
            self._smth_wrong(msg.chat.id)
            return

        goal: NewGoal = fsm_state.goal
        goal.due_date = str2date(msg.text)

        if not goal.due_date:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text="[wrong date or date format; should be yyyy-mm-dd]",
            )
            return

        if goal.complete():
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.cat_id,
                due_date=goal.due_date,
            )
            self.tg_client.send_message(chat_id=msg.chat.id, text="[new goal created]")
        else:
            self._smth_wrong(msg.chat.id)

        del_fsm_state(tg_user.chat_id)

    def handle_save_new_category(self, msg: Message, tg_user: TgUser):
        fsm_states = get_fsm_state(tg_user.chat_id)
        if not fsm_states:
            self._smth_wrong(msg.chat.id)
            return

        category = msg.text
        GoalCategory.objects.create(
            title=category, user_id=tg_user.user_id, board_id=fsm_states.board_id
        )
        self.tg_client.send_message(chat_id=msg.chat.id, text="[new category created]")
        del_fsm_state(tg_user.chat_id)

    def handle_delete_goal(self, msg: Message, tg_user: TgUser):
        set_fsm_state(
            tg_user.chat_id, FSMData(state=StateEnum.CHOOSE_GOAL, goal=NewGoal())
        )
        self.handle_goal_list(msg=msg, tg_user=tg_user)

    def handle_delete_selected_goal(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            goal_id = int(msg.text)
            goal = Goal.objects.filter(
                self._get_goal_query(tg_user, and_=Q(id=goal_id))
            ).first()
            if goal:
                goal.is_deleted = True
                goal.save(update_fields=["is_deleted"])
                self.tg_client.send_message(
                    chat_id=msg.chat.id, text="[goal has been deleted]"
                )
                del_fsm_state(tg_user.chat_id)
                return

        self.tg_client.send_message(chat_id=msg.chat.id, text="[invalid goal id]")

    def handle_mark_goal_done(self, msg: Message, tg_user: TgUser):
        set_fsm_state(
            tg_user.chat_id,
            FSMData(state=StateEnum.CHOOSE_GOAL_TO_DONE, goal=NewGoal()),
        )
        self.handle_goal_list(msg=msg, tg_user=tg_user)

    def handle_mark_selected_goal_done(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            goal_id = int(msg.text)
            goal = Goal.objects.filter(
                self._get_goal_query(tg_user, and_=Q(id=goal_id))
            ).first()
            if goal:
                goal.status = Goal.Status.done
                goal.save(update_fields=["status"])
                self.tg_client.send_message(
                    chat_id=msg.chat.id, text="[goal has been marked as done]"
                )
                del_fsm_state(tg_user.chat_id)
                return

        self.tg_client.send_message(chat_id=msg.chat.id, text="[invalid goal id]")

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if msg.text == "/goals":
            self.handle_goal_list(msg=msg, tg_user=tg_user)

        elif msg.text == "/cats":
            self.handle_category_list(msg=msg, tg_user=tg_user)

        elif msg.text == "/boards":
            self.handle_board_list(msg=msg, tg_user=tg_user)

        elif msg.text == "/create_goal":
            self.handle_create_goal(msg=msg, tg_user=tg_user)

        elif msg.text == "/create_cat":
            self.handle_create_category(msg=msg, tg_user=tg_user)

        elif msg.text == "/delete_goal":
            self.handle_delete_goal(msg=msg, tg_user=tg_user)

        elif msg.text == "/goal_done":
            self.handle_mark_goal_done(msg=msg, tg_user=tg_user)

        elif msg.text == "/cancel":
            del_fsm_state(tg_user.chat_id)

        elif fsm_state := get_fsm_state(tg_user.chat_id):
            state: StateEnum = fsm_state.state

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

            if state == StateEnum.CHOOSE_GOAL_TO_DONE:
                self.handle_mark_selected_goal_done(msg=msg, tg_user=tg_user)

        elif msg.text.startswith("/"):
            self.tg_client.send_message(chat_id=msg.chat.id, text="[unknown command]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=msg.chat.id,
            defaults={
                "username": msg.from_.username
                or str(msg.from_.first_name) + str(msg.from_.last_name)
            },
        )
        if created:
            self.tg_client.send_message(chat_id=msg.chat.id, text="[hello]")
        elif not tg_user.user:
            self.handle_user_wo_verification(msg=msg, tg_user=tg_user)
        else:
            self.handle_verified_user(msg=msg, tg_user=tg_user)
