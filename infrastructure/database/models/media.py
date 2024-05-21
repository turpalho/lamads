from typing import TYPE_CHECKING

from aiogram import types
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .users import User
    from .posts import Post


class Media(Base, TimestampMixin):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_id: Mapped[str]
    content_type: Mapped[types.ContentType] = mapped_column(Text)
    caption: Mapped[str | None]
    post_id: Mapped[int] = mapped_column(BigInteger,
                                         ForeignKey("posts.id", ondelete='CASCADE'))

    post: Mapped["Post"] = relationship(back_populates="")


def get_media_obj_from_messages(messages: list[types.Message], window_id: int):
    items: list[Media] = []
    for el in messages:
        caption = el.html_text
        content_type = el.content_type
        file_id = get_file_ids_from_message(el)
        if file_id:
            items.append(Media(file_id=file_id,
                               content_type=content_type,
                               caption=caption,
                               window_id=window_id))
    return items


def get_file_ids_from_message(message: types.Message):
    for value in message.__dict__.values():
        file_id = getattr(value, "file_id", None)
        if not file_id and hasattr(value, "__getitem__"):
            file_id = getattr(value[-1], "file_id", None)
        if file_id:
            return file_id
