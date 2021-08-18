allow_hosts = ['*']


def check_allowed_hosts(host):
    if allow_hosts is False:
        return 'access_is_allowed'
    if '*' in allow_hosts:
        return 'access_is_allowed'
    elif host in allow_hosts:
        return 'access_is_allowed'
    else:
        return 'access_not_allowed'
