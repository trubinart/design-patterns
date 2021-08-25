from framework.render import render
import datetime

class Index:
    def __call__(self,  *args, **kwargs):
        return '200 OK', render('index.html', data=datetime.datetime.today().strftime("%d.%m.%Y"))

class NoPage:
    def __call__(self,  *args, **kwargs):
        return "404 Not_Page", render('404.html')

class NotAccess:
    def __call__(self,  *args, **kwargs):
        return "401 Not_access", "You don't have access"

class Contacts:
    def __call__(self,  *args, **kwargs):
        return '200 OK', render('contacts.html')

