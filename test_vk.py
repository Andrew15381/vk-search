from vksearch.bot import vk_requests, vk_filters
from vkbottle.api import API
from vksearch.bot.config import VK_API_TOKEN
from vksearch.bot.limited_client import *
import pytest


@pytest.mark.asyncio
async def test_get_friends():
    api = API(VK_API_TOKEN, http_client=LimitSingleAiohttpClient())
    users = await vk_requests.get_friends(api, 168768958)
    assert len(users) == 252
    igor = vk_filters.filter_by(users, 'name', 'Azimov')[0]
    del igor['track_code']
    assert igor == {'id': 168516241,
                    'bdate': '18.6.2002',
                    'first_name': 'Igor',
                    'last_name': 'Azimov',
                    'can_access_closed': True,
                    'is_closed': False}
    await api.http_client.close()


@pytest.mark.asyncio
async def test_get_subs():
    api = API(VK_API_TOKEN, http_client=LimitSingleAiohttpClient())
    users = await vk_requests.get_subscriptions_members(api, 231819294)
    assert len(users) == 0
    await api.http_client.close()


def test_filter():
    a = [{'first_name': 'abc', 'last_name': 'bcd'},
         {'first_name': 'aaa', 'last_name': 'bca'},
         {'first_name': 'abc', 'last_name': 'aaa'}]
    assert vk_filters.filter_by(a, 'name', 'bcd') == [{'first_name': 'abc', 'last_name': 'bcd'}]
    a = [{'bdate': '1.1.1111'},
         {'bdate': '2.1.2111'},
         {'bdate': '1.1.1131'}]
    assert vk_filters.filter_by(a, 'bdate', '2.1.2') == [{'bdate': '2.1.2111'}]
    a = [{'id': 1, 'id': 1}]
    assert vk_filters.filter_by(a, 'id', None) == [{'id': 1}]
