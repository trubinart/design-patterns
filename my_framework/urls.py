from views import Index, NoPage, NotAccess, Contacts, \
    CreateCategory, CreateCourse, ChoseCopyCourse, CopyCourse

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    'no_page': NoPage(),
    'not_access': NotAccess(),
    '/create-category/': CreateCategory(),
    '/create-course/': CreateCourse(),
    '/choose-copy-course/': ChoseCopyCourse(),
    '/copy-course/': CopyCourse(),
}
