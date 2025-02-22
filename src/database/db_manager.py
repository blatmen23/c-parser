import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.schemas import Source as SourceSchemas, MediaContent as MediaContentSchemas, Post as PostSchema
from src.database.models import Posts, PostsTags, Tags, MediaContents, Sources, Comments
from src.database.database import connection

logger = logging.getLogger(__name__)

class DatabaseManager:

    async def _add_post(self, post: PostSchema, session: AsyncSession) -> int:
        """Добавляет пост и возвращает его ID"""
        post_orm = Posts(
            identifier=post.identifier,
            category=post.category,
            caption=post.caption,
            create_at=post.create_at
        )
        session.add(post_orm)
        await session.flush()
        return post_orm.id

    async def _add_media(self, post_id: int, media_list: list[MediaContentSchemas], session: AsyncSession):
        """Добавляет медиа для поста"""
        for media in media_list:
            session.add(MediaContents(
                post_id=post_id,
                media_type=media.file_type,
                media_url=media.media_url,
                file_type=media.file_type,
                file_size=media.file_size,
                file_hash=media.file_hash
            ))

    async def _add_source(self, post_id: int, source: SourceSchemas, session: AsyncSession):
        """Добавляет информацию об источнике"""
        session.add(Sources(
            post_id=post_id,
            url=source.url,
            platform=source.platform,
            posting_at=source.posting_at
        ))

    async def _add_tags(self, post_id: int, post_tags: list[str], session: AsyncSession):
        """Добавляет теги к посту"""
        tags_orm = [Tags(name=post_tag) for post_tag in post_tags]
        session.add_all(tags_orm)
        await session.flush()
        tag_ids = [tag_orm.id for tag_orm in tags_orm]

        for tag_id in tag_ids:
            session.add(PostsTags(
                post_id=post_id,
                tag_id=tag_id
            ))

    async def _add_comments(self, post_id: int, comments: list[str], session: AsyncSession):
        for capacity, comment in enumerate(comments):
            session.add(Comments(
                post_id=post_id,
                capacity=len(comments) - capacity,
                comment=comment
            ))

    @connection
    async def add_posts(self, posts: list[PostSchema], session: AsyncSession):
        for post in posts:
            post_id = await self._add_post(post, session)

            if post.media is not None:
                await self._add_media(post_id, post.media, session)

            await self._add_source(post_id, post.source, session)

            if post.comments is not None:
                await self._add_comments(post_id, post.comments, session)

            if post.posts_tags is not None:
                await self._add_tags(post_id, post.posts_tags, session)
        await session.commit()

