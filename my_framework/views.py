from framework.render import render
import datetime
from patterns.create_patterns import Engine, Logger, MainCategory, MainCategoryPrototype
from patterns.structure_patterns import AppRoute, Debug

site = Engine()
main_category = MainCategoryPrototype()
day = datetime.datetime.today().strftime("%d.%m.%Y")

logger = Logger('views')

routes = {}

@AppRoute(routes, '/')
class Index:
    @Debug(name='Index')
    def __call__(self, *args, **kwargs):
        return '200 OK', render('index.html', data=day, objects_list=site.courses)

@AppRoute(routes, 'no_page')
class NoPage:
    @Debug(name='NoPage')
    def __call__(self, *args, **kwargs):
        return "404 Not_Page", render('404.html')

@AppRoute(routes, 'not_access')
class NotAccess:
    @Debug(name='NotAccess')
    def __call__(self, *args, **kwargs):
        return "401 Not_access", "You don't have access"

@AppRoute(routes, '/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, *args, **kwargs):
        return '200 OK', render('contacts.html')

@AppRoute(routes, '/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']

            name = data['category_name']
            category_id = data['category_id']
            main_category_name = data['main_category']

            if main_category_name not in main_category.all_main_category_name:
                new_main_category = MainCategory(main_category_name)
            else:
                new_main_category = main_category.get_main_gategory(main_category_name)

            new_category = site.create_category(name, category_id)
            new_main_category.add(new_category)

            site.categories.append(new_category)
            logger.write(f'Создана категория | {name} | ID {category_id}')
            return '200 OK', render('index.html', objects_list=site.courses, data=day)
        else:
            return '200 OK', render('create_category.html')

@AppRoute(routes, '/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            category_id = data['category_id']
            course_type = data['type']

            if course_type == 'life':
                place = data['place_offline']

            elif course_type == 'online':
                place = data['place_online']
            else:
                place = None

            for item in site.categories:
                if int(category_id) == item.id:
                    category = item
                    course = site.create_course(course_type, name, category, place)
                    site.courses.append(course)
                    logger.write(f'Создан курc| {category} | {name} '
                                 f'| {course_type} | место {place}')
            return '200 OK', render('index.html', objects_list=site.courses, data=day)

        else:
            return '200 OK', render('create_course.html', objects_list=site.categories)

@AppRoute(routes, '/choose-copy-course/')
class ChoseCopyCourse:
    @Debug(name='ChoseCopyCourse')
    def __call__(self, *args, **kwargs):
        return '200 OK', render('choose_copy_course.html', objects_list=site.courses)

@AppRoute(routes, '/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        name_course = request['data']['course_for_copy']
        new_course = object
        for item in site.courses:
            if item.name == name_course:
                new_course = item.clone()
        site.courses.append(new_course)
        return '200 OK', render('index.html', objects_list=site.courses, data=day)




# class CopyCourse:
#     def __call__(self, request):
#         course_places = {}
#         type_place = ''
#         type_course = ''
#         course = object
#
#         for course in site.courses:
#             if course.name == request['data']['course_for_copy']:
#                 course_places = (course.all_place)
#
#             if course.__class__.__name__ == 'LifeCourse':
#                 type_place = 'place_offline'
#                 type_course = 'life'
#
#             if course.__class__.__name__ == 'OnlineCourse':
#                 type_place = 'place_online'
#                 type_course = 'online'
#
#         return '200 OK', render('copy_course.html', item=course, objects_list=site.categories,
#                                 places=course_places, type_place=type_place, type_course=type_course)
