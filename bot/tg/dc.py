from typing import List, Optional

from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: int
    type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None


class MessageFrom(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str


class Message(BaseModel):
    message_id: int
    from_: MessageFrom = Field(alias="from")
    chat: Chat
    text: Optional[str] = None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: List[UpdateObj]  # todo


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message  # todo
