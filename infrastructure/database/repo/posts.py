import logging
import os
from typing import TYPE_CHECKING, Optional, Dict

from sqlalchemy import delete, select, update, ScalarResult
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Post, Media
from infrastructure.database.repo.base import BaseRepo



class PostRepo(BaseRepo):
    model = Post

    async def add_post(self,
                       text: str | None,
                       user_id: int,
                       channel_id: int,
                       media_list: list[Dict] | None = None) -> None:
        """
        Creates a new post in the database and returns the post object.

        Args:
            title (str): The unique heading of the post.
            user_id (int): The unique identifier of the user who created the post.
            text (Optional[str]): The text content of the post.
            media_list (Optional[list[str]]): IDs of files attached to the post.

        Returns:
            Post: The Post object.
        """

        post = Post(user_id=user_id,
                    text=text,
                    channel_id=channel_id)

        if media_list:
            for media_file in media_list:
                media = Media(
                    file_id=media_file['file_id'],
                    content_type=media_file['content_type']
                    )
                post.media.append(media)

        self.session.add(post)
        await self.session.commit()

    async def get_all_posts(self,
                            user_id: int) -> ScalarResult[Post]:
        stmt = select(Post).where(
            Post.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_posts_with_files(self,
                                        user_id: int) -> ScalarResult[Post]:
        stmt = select(Post).where(
            Post.user_id == user_id).options(selectinload(Post.files))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_post(self, post_id: int) -> Post | None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_post_with_files(self, post_id: int) -> Post | None:
        stmt = select(Post).where(
            Post.id == post_id).options(selectinload(Post.files))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_post(self, post_id: int) -> None:
        post = await self.get_post_with_files(post_id)
        if post:
            stmt = delete(Post).where(Post.id == post_id)
            await self.session.execute(stmt)
            await self.session.commit()
        return