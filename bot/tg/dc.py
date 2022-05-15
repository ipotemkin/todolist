from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    pass


@dataclass
class UpdateObj:
    pass


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]  # todo

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message  # todo

    class Meta:
        unknown = EXCLUDE