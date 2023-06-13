"""Contains tools for http requests limiting."""

import asyncio
from abc import ABCMeta
from functools import wraps
from vkbottle.http import SingleAiohttpClient


class AsyncLimit:
    """Limits async function calls per period."""

    limits = dict()

    def __init__(self, limit_id: str, limit: int, period: int):
        """Stores period and limit to dict for later use.

        :param limit_id: limit id for multiple limits support
        :type msg: str

        :param limit: calls limit per period
        :type limit: int

        :param period: period in seconds
        :type period: int
        """
        self.id = limit_id
        self.limit = limit
        if limit_id not in AsyncLimit.limits:
            AsyncLimit.limits[limit_id] = [limit, period]

    def __call__(self, func):
        """Wraps func for calls limiting per period

        :param func: func to limit
        :type func: callable

        :return: callable
        """
        @wraps(func)
        async def limited_func(*args, **kwargs):
            if AsyncLimit.limits[self.id][0] == 0:
                await asyncio.sleep(AsyncLimit.limits[self.id][1])
                AsyncLimit.limits[self.id][0] = self.limit

            AsyncLimit.limits[self.id][0] -= 1

            return await func(*args, **kwargs)
        return limited_func


class MetaLimitClient(ABCMeta):
    """Limits required client functions (see aiohttp doc) with AsyncLimit decorator."""

    def __new__(cls, name, bases, attrs, limit_id: str, limit: int, period: int):
        """Modifies class instance with AsyncLimit.

        :param cls: class to limit
        :type cls: class

        :param name: class name
        :type name: str

        :param bases: class bases
        :type bases: list

        :param attrs: instance attrs
        :type attrs: dict

        :param limit_id: limit_id in AsyncLimit dict
        :type limit_id: str

        :param limit: calls limit
        :type limit: int

        :param period: period in seconds
        :type period: int

        :return: decorated cls instance
        """
        instance = super().__new__(cls, name, bases, attrs)
        instance.request_raw = AsyncLimit(limit_id, limit, period)(instance.request_raw)
        instance.request_json = AsyncLimit(limit_id, limit, period)(instance.request_json)
        instance.request_text = AsyncLimit(limit_id, limit, period)(instance.request_text)
        instance.request_content = AsyncLimit(limit_id, limit, period)(instance.request_content)
        return instance


class LimitSingleAiohttpClient(SingleAiohttpClient, metaclass=MetaLimitClient, limit_id='vk', limit=5, period=1):
    """Limits vkbottle.http.SingleAiohttpClient for 5 calls per second."""

    pass
