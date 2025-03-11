import asyncio
import logging
from datetime import datetime, timedelta
import re
import json

from playwright.async_api import Browser
from bs4 import BeautifulSoup

from src.crawler.scrappers.scrapper import Scrapper
from src.schemas.schemas import Post, MediaContent, Source
from src.schemas.enums import Platforms, MediaTypes

logger = logging.getLogger(__name__)


class NineGagScrapper(Scrapper):
    def __init__(self, browser: Browser, urls: list[str] = None):
        default_urls = ["https://9gag.com/"]
        super().__init__(browser, urls or default_urls)

