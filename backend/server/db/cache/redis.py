from typing import Any

import redis.asyncio as aioredis

from server.config.settings import DefaultSettings


class Cache:
    def __init__(self):
        self.__redis = aioredis.from_url(DefaultSettings().CACHE_URL, encoding="utf-8", decode_responses=True)

    def get_connection(self):
        return self.__redis

    async def set(self, key: str, value: Any):
        await self.__redis.set(key, value)

    async def get(self, key: str):
        return await self.__redis.get(key)
