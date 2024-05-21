from datetime import timedelta
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .users import User
    from .posts import Post


class Channel(Base, TimestampMixin):
    __tablename__ = "channels"

    channel_id: Mapped[int] = mapped_column(primary_key=True,
                                            index=True,
                                            type_=BigInteger)
    name: Mapped[Optional[str]] = mapped_column(index=True)
    url: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    bot_is_on: Mapped[Optional[bool]] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(BigInteger,
                                         ForeignKey("users.user_id", ondelete='CASCADE'),
                                        nullable=False)

    user: Mapped["User"] = relationship(back_populates="channels")
    posts: Mapped[list["Post"]] = relationship(back_populates="channel")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        return f"Channel: #{self.channel_id}"
