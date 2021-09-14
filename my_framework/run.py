from wsgiref.simple_server import make_server
from framework.main import Framework
from views import routes


application = Framework(routes)
port = 8000

with make_server('', port, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()