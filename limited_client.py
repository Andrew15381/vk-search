import asyncio
from abc import ABCMeta
from functools import wraps
from vkbottle.http import SingleAiohttpClient


class AsyncLimit:
    limits = dict()

    def __init__(self, limit_id, limit, period):
        self.id = limit_id
        self.limit = limit
        if limit_id not in AsyncLimit.limits:
            AsyncLimit.limits[limit_id] = [limit, period]

    def __call__(self, func):
        @wraps(func)
        async def limited_func(*args, **kwargs):
            if AsyncLimit.limits[self.id][0] == 0:
                await asyncio.sleep(AsyncLimit.limits[self.id][1])
                AsyncLimit.limits[self.id][0] = self.limit

            AsyncLimit.limits[self.id][0] -= 1

            return await func(*args, **kwargs)
        return limited_func


class MetaLimitClient(ABCMeta):
    def __new__(cls, name, bases, attrs, limit_id, limit, period):
        instance = super().__new__(cls, name, bases, attrs)
        instance.request_raw = AsyncLimit(limit_id, limit, period)(instance.request_raw)
        instance.request_json = AsyncLimit(limit_id, limit, period)(instance.request_json)
        instance.request_text = AsyncLimit(limit_id, limit, period)(instance.request_text)
        instance.request_content = AsyncLimit(limit_id, limit, period)(instance.request_content)
        return instance


class LimitSingleAiohttpClient(SingleAiohttpClient, metaclass=MetaLimitClient, limit_id='vk', limit=5, period=1):
    pass
