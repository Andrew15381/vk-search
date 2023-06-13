"""Bot main, contains commands' handlers."""

import config
from limited_client import LimitSingleAiohttpClient
from vk_requests import get_friends, get_subscriptions_members
from vk_filters import filter_by
from vkbottle import API
from aiogram import Bot, Dispatcher, executor, types, filters


bot = Bot(token=config.TG_API_TOKEN)
dp = Dispatcher(bot)
api = API(token=config.VK_API_TOKEN, http_client=LimitSingleAiohttpClient())


@dp.message_handler(commands=['help', 'start'])
async def start(message: types.Message) -> None:
    """Handles help and start commands, outputs help message with commands description.

    :param message: message object
    :type message: aiogram.type.Message
    """
    with open('help.txt', 'r') as file:
        mes = file.read()
    await message.answer(mes)


@dp.message_handler(commands=['search'])
async def search(message: types.Message, command: filters.Command.CommandObj) -> None:
    """Handles search command.

    Parameters: user_id and modificators.
    Modificators are applied step by step.
    Available modificators:
        friends (add current users' friends to next step),
        subs (add current users' groups subs to next step),
        name (filter current users by name part, both first and last),
        bdate (filter current users by bdate part).
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
            await message.answer("Найдено больше 100 пользователей, уточните запрос")
        else:
            for user in users:
                await message.answer(f"http://vk.com/id{user['id']}")
    else:
        await message.answer("Укажите аккаунт для старта и набор расширений/фильтров")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
