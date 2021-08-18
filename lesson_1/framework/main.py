from pprint import pprint
from .middleware import check_allowed_hosts


class Framework:
    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):

        # Беру хост из environ
        host = environ['REMOTE_ADDR']

        # Проверяю разрешенные хосты
        check_hosts = check_allowed_hosts(host)

        if check_hosts == 'access_not_allowed':
            view = self.routes.get('not_access')
            response_code, response_body = view()
            headers = [('Content-Type', 'text/html')]
            start_response(response_code, headers)
            return [response_body.encode('utf-8')]

        # Беру путь из environ
        url = environ['PATH_INFO']

        # Проверяю на слеш в конце. Добавляю, если его нет
        if not url.endswith('/'):
            url = f'{url}/'

        # Достаю views из списка routers
        if url in self.routes:
            view = self.routes.get(url)
        else:
            view = self.routes.get('no_page')

        # Возвращаю ответ
        response_code, response_body = view()
        headers = [('Content-Type', 'text/html')]
        start_response(response_code, headers)
        return [response_body.encode('utf-8')]

