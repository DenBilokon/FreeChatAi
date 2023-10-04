import datetime

from pydantic import BaseModel, Field


class ChatHistoryBase(BaseModel):
    message: str = Field(max_length=5000)


class ChatHistoryModel(ChatHistoryBase):
    id: int
    created_at: datetime.datetime | None
    user_id: int
    chat_id: int

    class Config:
        from_attributes = True
