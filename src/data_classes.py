import datetime

from enums import *
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class MediaContent:
    media_type: MediaTypes
    file_type: FileTypes
    media_url: str
    media_hash: Optional[str]

@dataclass
class Source:
    url: str
    platform: Platforms
    posting_at: int

@dataclass
class Post:
    identifier: str
    category: Optional[Categories]
    media: Optional[list[MediaContent]]
    comments: Optional[list[str]]
    source: Source
    title: Optional[str]
    caption: Optional[str]
    create_at: int
    posts_tags: Optional[list[str]]
