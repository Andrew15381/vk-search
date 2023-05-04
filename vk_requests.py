from vkbottle import vkscript, API

MAX_MEMS_TOTAL = 25000  # vkscript can't send more than 5 mb
MAX_MEMS_SINGLE = 1000  # get_members returns less than 1000 members


@vkscript
def get_members(api, group_id: int, offset: int, count: int, per_req: int):
    total_mems = []
    i = offset
    while i + per_req <= offset + count:
        mems = api.groups.get_members(group_id=group_id, offset=i, count=per_req).items
        total_mems.extend(mems)
        i += per_req
    if count % per_req != 0:
        mems = api.groups.get_members(group_id=group_id, offset=count / per_req * per_req, count=count % per_req).items
        total_mems.extend(mems)
    return {'items': total_mems}


async def get_subscriptions_members(api: API, user_id: int):
    try:
        subs = await api.users.get_subscriptions(user_id=user_id)
    except:
        return []  # private profile
    subs = subs.groups.items  # list of sub ids
    total_mems = []
    for sub in subs:
        mems = await api.groups.get_members(group_id=sub)  # set of mem ids
        total_mems.extend(mems.items)
        total_mems_count = mems.count
        for i in range(MAX_MEMS_SINGLE, total_mems_count - MAX_MEMS_TOTAL + 1, MAX_MEMS_TOTAL):
            mems = await api.execute(code=get_members(group_id=sub, offset=i, count=MAX_MEMS_TOTAL,
                                                      per_req=MAX_MEMS_SINGLE))  # vkscript handles 25 requests
            total_mems.extend(mems['response']['items'])
        if total_mems_count % MAX_MEMS_TOTAL != 0:
            mems = await api.execute(code=get_members(group_id=sub,
                                                      offset=((total_mems_count - MAX_MEMS_SINGLE) // MAX_MEMS_TOTAL *
                                                              MAX_MEMS_TOTAL + MAX_MEMS_SINGLE),
                                                      count=(total_mems_count - MAX_MEMS_SINGLE) % MAX_MEMS_TOTAL,
                                                      per_req=MAX_MEMS_SINGLE))
            total_mems.extend(mems['response']['items'])
    return total_mems
