from pprint import pprint
from .middleware import check_allowed_hosts
from .requests import GetRequest, PostRequest

import sys

sys.path.append("..")
from patterns.patterns import Logger

logger = Logger('main')


class Framework:
    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):
        request = {}

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

        # Беру метод запроса и обрабатываю его
        method = environ['REQUEST_METHOD']

        if method == 'GET' and environ['QUERY_STRING']:
            data = GetRequest().split_params(environ['QUERY_STRING'])
            request['data'] = data
            request['path'] = url
            logger.write(f'{method} | {url} | {data}')

        if method == 'POST' and environ['CONTENT_LENGTH']:
            data = PostRequest().get_bytes(environ)
            request['data'] = data
            request['path'] = url
            logger.write(f'{method} | {url} | {data}')


        # Возвращаю ответ
        request['method'] = environ['REQUEST_METHOD']
        response_code, response_body = view(request)
        headers = [('Content-Type', 'text/html')]
        start_response(response_code, headers)
        return [response_body.encode('utf-8')]
