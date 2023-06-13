from vkbottle import API, vkscript

MAX_MEMS_TOTAL = 20000  # vkscript can't send more than 5 mb
MAX_MEMS_SINGLE = 1000  # get_members returns less than 1000 members

MAX_FRIENDS_TOTAL = 20000
MAX_FRIENDS_SINGLE = 5000  # get_friends returns less than 5000 friends


@vkscript
def get_members_script(api, group_id: int, offset: int, count: int, per_req: int) -> dict:
    total_mems = []
    i = offset
    while i + per_req <= offset + count:
        mems = api.groups.get_members(group_id=group_id, offset=i, count=per_req, fields=['bdate']).items
        total_mems.extend(mems)
        i += per_req
    if count % per_req != 0:
        tail_start = count - count % per_req
        mems = api.groups.get_members(group_id=group_id,
                                      offset=offset + tail_start,
                                      count=count % per_req,
                                      fields=['bdate']).items
        total_mems.extend(mems)
    return {'items': total_mems}


async def get_subscriptions_members(api: API, user_id: int) -> list:
    try:
        subs = await api.users.get_subscriptions(user_id=user_id)
    except:
        return []  # private profile
    subs = subs.groups.items  # list of sub ids
    total_mems = []
    for sub in subs:
        try:
            mems = await api.groups.get_members(group_id=str(sub))  # private group
        except:
            continue
        total_mems.extend(mems.items)
        total_mems_count = mems.count
        for i in range(MAX_MEMS_SINGLE, total_mems_count - MAX_MEMS_TOTAL + 1, MAX_MEMS_TOTAL):
            mems = await api.execute(code=get_members_script(group_id=sub, offset=i, count=MAX_MEMS_TOTAL,
                                                             per_req=MAX_MEMS_SINGLE))  # vkscript handles 25 requests
            total_mems.extend(mems['response']['items'])
        if (total_mems_count - MAX_MEMS_SINGLE) % MAX_MEMS_TOTAL != 0:
            mems = await api.execute(code=get_members_script(group_id=sub,
                                                             offset=((total_mems_count - MAX_MEMS_SINGLE) // MAX_MEMS_TOTAL *
                                                                     MAX_MEMS_TOTAL + MAX_MEMS_SINGLE),
                                                             count=(total_mems_count - MAX_MEMS_SINGLE) % MAX_MEMS_TOTAL,
                                                             per_req=MAX_MEMS_SINGLE))
            total_mems.extend(mems['response']['items'])
    return total_mems


@vkscript
def get_friends_script(api, user_id: int, offset: int, count: int, per_req: int) -> list:
    total_friends = []
    i = offset
    while i + per_req <= offset + count:
        friends = api.friends.get(user_id=user_id, offset=i, count=per_req, fields=['bdate'], lang='ru').items
        total_friends.extend(friends)
        i += per_req
    if count % per_req != 0:
        tail_start = count - count % per_req
        friends = api.friends.get(user_id=user_id,
                                  offset=offset + tail_start,
                                  count=count % per_req,
                                  fields=['bdate']).items
        total_friends.extend(friends)
    return {'items': total_friends}

    
async def get_friends(api: API, user_id: int) -> list:
    try:
        response = await api.friends.get(user_id=user_id)
        total_friends_count = response.count
    except:
        return []
    total_friends = []
    for i in range(0, total_friends_count - MAX_FRIENDS_TOTAL + 1, MAX_FRIENDS_TOTAL):
        friends = await api.execute(code=get_friends_script(user_id=user_id, offset=i, count=MAX_FRIENDS_TOTAL,
                                                            per_req=MAX_FRIENDS_SINGLE))  # vkscript handles 25 requests
        total_friends.extend(friends['response']['items'])
    if total_friends_count % MAX_FRIENDS_TOTAL != 0:
        friends = await api.execute(code=get_friends_script(user_id=user_id,
                                                            offset=(total_friends_count // MAX_FRIENDS_TOTAL *
                                                                    MAX_FRIENDS_TOTAL),
                                                            count=total_friends_count % MAX_FRIENDS_TOTAL,
                                                            per_req=MAX_FRIENDS_SINGLE))
        total_friends.extend(friends['response']['items'])
    return total_friends

