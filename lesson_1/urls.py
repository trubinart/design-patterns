from views import Index, NoPage, NotAccess

routes = {
    '/': Index(),
    'no_page': NoPage(),
    'not_access': NotAccess(),
}
