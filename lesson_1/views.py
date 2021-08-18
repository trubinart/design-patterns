from framework.render import render

class Index:
    def __call__(self,  *args, **kwargs):
        return '200 OK', render('index.html')

class No_page:
    def __call__(self,  *args, **kwargs):
        return "404 Not_Page", render('404.html')

class Not_access:
    def __call__(self,  *args, **kwargs):
        return "401 Not_access", "You don't have access"

