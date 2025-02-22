from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import text, String, LargeBinary, TIMESTAMP, DATETIME, ForeignKey

from src.database.overbuilds import intpk, str_32, str_64, str_128, str_256, str_512
from src.schemas.enums import Platforms, Categories, MediaTypes, FileTypes

from typing import Optional


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
    identifier: Mapped[str_256] # = mapped_column(unique=True)
    category: Mapped[Optional[Categories]]
    caption: Mapped[Optional[str_512]]
    create_at: Mapped[DATETIME] = mapped_column(DATETIME)

    media_contents: Mapped[list["MediaContents"]] = relationship(back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship(back_populates="posts")
    sources: Mapped["Sources"] = relationship(back_populates="posts")
    posts_tags: Mapped["PostsTags"] = relationship(back_populates="posts")


class MediaContents(Base):
    __tablename__ = "media_contents"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    media_type: Mapped[MediaTypes]
    media_url: Mapped[str_512]
    file_type: Mapped[FileTypes]
    file_size: Mapped[int]
    file_hash: Mapped[str_128]  # = mapped_column(unique=True)

    posts: Mapped["Posts"] = relationship(back_populates="media_contents")


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    capacity: Mapped[int] = mapped_column()
    comment: Mapped[str_256]

    posts: Mapped["Posts"] = relationship(back_populates="comments")


class Sources(Base):
    __tablename__ = "sources"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    url: Mapped[str_512]
    platform: Mapped[Platforms]
    posting_at: Mapped[DATETIME] = mapped_column(DATETIME)

    posts: Mapped["Posts"] = relationship(back_populates="sources")