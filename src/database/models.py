from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import text, String, LargeBinary, TIMESTAMP, ForeignKey

from .overbuilds import intpk, str_32, str_64, str_128, str_256, str_512
from ..enums import Platforms, Categories, MediaTypes, FileTypes

class Base(DeclarativeBase):
    type_annotation_map = {
        str_32: String(32),
        str_64: String(64),
        str_128: String(128),
        str_256: String(256),
        str_512: String(512)
    }

class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[intpk]
    name: Mapped[str_64]

class PostsTags(Base):
    __tablename__ = "posts_tags"

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="RESTRICT"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="RESTRICT"))

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[intpk]
    category: Mapped[Categories]
    media_id: Mapped[int] = mapped_column(ForeignKey("media_contents.id", ondelete="CASCADE"))
    comments_id: Mapped[int] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"))
    caption: Mapped[str_512]
    create_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class MediaContents(Base):
    __tablename__ = "media_contents"

    sur_id: Mapped[intpk]
    id: Mapped[int]
    media_type: Mapped[MediaTypes]
    file_type: Mapped[FileTypes]
    binary_data: Mapped[LargeBinary] = mapped_column(LargeBinary)

class Comments(Base):
    __tablename__ = "comments"

    sur_id: Mapped[intpk]
    id: Mapped[int]
    rating: Mapped[int]
    comment: Mapped[str_256]
    media_id: Mapped[int] = mapped_column(ForeignKey("media_contents.id", ondelete="CASCADE"))

class Sources(Base):
    __tablename__ = "sources"

    id: Mapped[intpk]
    url: Mapped[str_512]
    platform: Mapped[Platforms]
    posting_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP)
