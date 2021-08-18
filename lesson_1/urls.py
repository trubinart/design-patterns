from views import Index, No_page, Not_access

routes = {
    '/': Index(),
    'no_page': No_page(),
    'not_access': Not_access(),
}
