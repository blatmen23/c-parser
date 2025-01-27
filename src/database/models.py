from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import text, String, Integer, LargeBinary, TIMESTAMP, ForeignKey

from src.database.overbuilds import intpk, str_32, str_64, str_128, str_256, str_512
from src.enums import Platforms, Categories, MediaTypes, FileTypes

from typing import Optional, List

class Base(DeclarativeBase):
    type_annotation_map = {
        str_32: String(32),
        str_64: String(64),
        str_128: String(128),
        str_256: String(256),
        str_512: String(512)
    }

class PostsTags(Base):
    __tablename__ = "posts_tags"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))

    tags: Mapped[list["Tags"]] = relationship(back_populates="posts_tags")
    posts: Mapped[list["Posts"]] = relationship(back_populates="posts_tags")

class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[intpk]
    name: Mapped[str_32]

    posts_tags: Mapped["PostsTags"] = relationship(back_populates="tags")

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[intpk]
    category: Mapped[Optional[Categories]]
    media_id: Mapped[Optional[int]] = mapped_column(unique=True)
    comments_id: Mapped[Optional[int]] = mapped_column(unique=True)
    source_id: Mapped[int] = mapped_column(unique=True)
    caption: Mapped[Optional[str_512]]
    create_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    media_contents: Mapped[list["MediaContents"]] = relationship(back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship(back_populates="posts")
    source: Mapped["Sources"] = relationship(back_populates="posts")
    posts_tags: Mapped["PostsTags"] = relationship(back_populates="posts")


class MediaContents(Base):
    __tablename__ = "media_contents"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    media_type: Mapped[MediaTypes]
    file_type: Mapped[FileTypes]
    binary_data: Mapped[LargeBinary] = mapped_column(LargeBinary)

    post: Mapped["Posts"] = relationship(back_populates="media_contents")


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    rating: Mapped[int]
    comment: Mapped[str_256]
    media_id: Mapped[Optional[int]] = mapped_column(ForeignKey("media_contents.id", ondelete="CASCADE"))

    post: Mapped["Posts"] = relationship(back_populates="comments")


class Sources(Base):
    __tablename__ = "sources"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    url: Mapped[str_512]
    platform: Mapped[Platforms]
    posting_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP)

    post: Mapped["Posts"] = relationship(back_populates="sources")