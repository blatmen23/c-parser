from aiohttp import ClientSession, ClientTimeout

from src.schemas.schemas import Post, MediaContent

class MediaDownloader:
    def __init__(self, posts: list[Post]):
        self.posts = posts

    async def _download_file(self, session: ClientSession):
        for post in self.posts:
            if post.media is not None:
                for media in post.media:
                    async with session.get(media.media_url) as response:
                        response.raise_for_status()
                        with open("fill.webm", 'wb') as f:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f.write(chunk)

    async def download_media(self):
        async with ClientSession(trust_env=True, timeout=ClientTimeout(total=5)) as session:
            await self._download_file(session)

        return self.posts