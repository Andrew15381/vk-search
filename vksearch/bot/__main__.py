"""Bot main, contains commands' handlers."""

from .config import TG_API_TOKEN, VK_API_TOKEN
from .limited_client import LimitSingleAiohttpClient
from .vk_requests import get_friends, get_subscriptions_members
from .vk_filters import filter_by
from vkbottle import API
from aiogram import Bot, Dispatcher, executor, types, filters
import gettext
import os.path

tr = gettext.translation('bot', os.path.dirname(__file__) + '/vksearch/bot/po', languages=['ru'])
tr.install()
_ = tr.gettext

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)
api = API(token=VK_API_TOKEN, http_client=LimitSingleAiohttpClient())


@dp.message_handler(commands=['help', 'start'])
async def start(message: types.Message) -> None:
    """Handles help and start commands, outputs help message with commands description.

    :param message: message object
    :type message: aiogram.type.Message
    """
    await message.answer(_("""Commands list:
/start - start bot
/help - show this message
/search - search among user's friends or groups' subs

The search is performed step by step, starting from user_id and continuing with a set of modificators:
* friends (add current users' friends to next step),
* subs (add current users' groups subs to next step),
* name (filter current users by name part, both first and last),
* bdate (filter current users by bdate part).

Example:
/search 168768958 friends name("Azimov")"""))


@dp.message_handler(commands=['search'])
async def search(message: types.Message, command: filters.Command.CommandObj) -> None:
    """Handles search command.

    Parameters: user_id and modificators.
    Modificators are applied step by step.
    Available modificators:

    * friends (add current users' friends to next step),

    * subs (add current users' groups subs to next step),

    * name (filter current users by name part, both first and last),

    * bdate (filter current users by bdate part).

    Checks parameters for errors.

    :param message: message object
    :type msg: aiogram.type.Message

    :param command: command object
    :type command: aiogram.filters.Command.CommandObj
    """
    if command.args:
        args = command.args.split()
        user_id, mods = int(args[0]), args[1:]
        users = [{'id': user_id, 'bdate': '0.0.0000', 'first_name': '', 'last_name': ''}]
        for mod in mods:
            new_users_total = []
            if mod == 'friends':
                for user in users:
                    new_users = await get_friends(api, user['id'])
                    new_users_total += new_users
            elif mod == 'subs':
                for user in users:
                    new_users = await get_subscriptions_members(api, int(user['id']))
                    new_users_total += new_users
            elif mod.startswith('name') and len(mod) > 8:
                name = mod[6:-2]
                new_users_total += filter_by(users, 'name', name)
            elif mod.startswith('bdate') and len(mod) > 9:
                bdate = mod[7:-2]
                new_users_total += filter_by(users, 'bdate', bdate)
            users = filter_by(new_users_total, 'id', None)
        if len(users) > 100:
            await message.answer(_("Found more than 100 users, try to narrow the search"))
        else:
            for user in users:
                await message.answer(f"http://vk.com/id{user['id']}")
    else:
        await message.answer(_("Enter a user id and a set of modifications to start"))


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
