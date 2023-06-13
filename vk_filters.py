def filter_by(users, field, value):
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
