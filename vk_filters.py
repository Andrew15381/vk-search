"""Contains tools for users filtering."""


def filter_by(users: list, field: str, value: str) -> list:
    """Filters out some users based on field:

        name - search for value substring in full name,
        bdate - search for value substring in bdate,
        id - leave users with unique ids.

    :param users: users list to filter
    :type users: list

    :param field: field to filter by
    :type field: str

    :param value: value to filter by
    :type value: str

    :return: list
    """
    ids = set()
    res = []
    for user in users:
        if field == 'name':
            name = user['last_name'] + ' ' + user['first_name']
            if value in name:
                res.append(user)
        elif field == 'bdate':
            if value in user['bdate']:
                res.append(user)
        elif field == 'id':
            if user['id'] not in ids:
                ids.add(user['id'])
                res.append(user)
    return res
