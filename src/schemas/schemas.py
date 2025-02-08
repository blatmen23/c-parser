import datetime
from typing_extensions import Annotated

from pydantic import BaseModel, Field, HttpUrl, field_validator

from .enums import Platforms, Categories, MediaTypes, FileTypes

class MediaContent(BaseModel):
    media_type: MediaTypes
    file_type: FileTypes
    media_url: HttpUrl
    media_hash: str | None

class Source(BaseModel):
    url: HttpUrl
    platform: Platforms
    posting_at: datetime.datetime

class Post(BaseModel):
    identifier: str
    category: Categories | None
    media: list[MediaContent] | None
    comments: list[str] | None
    source: Source
    title: str
    caption: str | None
    create_at: datetime.datetime
    posts_tags: list[str] | None

    @field_validator('media', 'comments', mode='before')
    def convert_empty_list_to_none(cls, v):
        if isinstance(v, list) and len(v) == 0:
            return None
        return v