import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator
from .enums import Platforms, Categories, MediaTypes, FileTypes

class MediaContent(BaseModel):
    """file_size: int [bytes]"""
    media_type: MediaTypes
    media_url: str
    file_type: FileTypes
    file_size: int
    file_hash: str | None

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