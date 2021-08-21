from views import Index, NoPage, NotAccess, Contacts

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    'no_page': NoPage(),
    'not_access': NotAccess(),
}
