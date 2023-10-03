import datetime

from pydantic import BaseModel, Field


class ChatBase(BaseModel):
    title_chat: str = Field(max_length=500)
    file_url: str | None
    chat_data: str | None


class ChatModel(ChatBase):
    id: int
    # file_url: str | None
    # chat_data: str = Field()
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    user_id: int

    class Config:
        from_attributes = True


class ChatUpdate(ChatModel):
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
