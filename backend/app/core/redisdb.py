from redis.asyncio import Redis
import json
from typing import Any
from .config import settings

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)


class RedisService:
    def __init__(self, client: Redis):
        self.client = client

    async def get(self, key: str) -> str | None:
        return await self.client.get(key)

    async def set(
        self,
        key: str,
        value: str,
        *,
        expire: int | None = None,
    ) -> None:
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self.client.exists(key))

    async def set_json(
        self,
        key: str,
        value: dict[str, Any],
        *,
        expire: int | None = None,
    ) -> None:
        await self.client.set(
            key,
            json.dumps(value),
            ex=expire,
        )

    async def get_json(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        value = await self.client.get(key)
        if value is None:
            return None

        return json.loads(value)


redis_service = RedisService(redis)
__all__ = ["redis_service"]
