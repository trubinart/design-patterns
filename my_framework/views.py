from framework.render import render
import datetime
from patterns.patterns import Engine, Logger

site = Engine()
day = datetime.datetime.today().strftime("%d.%m.%Y")

logger = Logger('views')


class Index:
    def __call__(self, *args, **kwargs):
        return '200 OK', render('index.html', data=day, objects_list=site.courses)


class NoPage:
    def __call__(self, *args, **kwargs):
        return "404 Not_Page", render('404.html')


class NotAccess:
    def __call__(self, *args, **kwargs):
        return "401 Not_access", "You don't have access"


class Contacts:
    def __call__(self, *args, **kwargs):
        return '200 OK', render('contacts.html')


class CreateCategory:

    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']

            name = data['category_name']

            category_id = data.get('category_id')

            new_category = site.create_category(name, category_id)

            site.categories.append(new_category)
            logger.write(f'Создана категория | {name} | ID {category_id}')
            return '200 OK', render('index.html', objects_list=site.courses, data=day)
        else:
            return '200 OK', render('create_category.html')


class CreateCourse:
    category_id = -1

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


class ChoseCopyCourse:
    def __call__(self, *args, **kwargs):
        return '200 OK', render('choose_copy_course.html', objects_list=site.courses)


class CopyCourse:
    def __call__(self, request):
        course_places = {}
        type_place = ''
        type_course = ''
        course = object

        for course in site.courses:
            if course.name == request['data']['course_for_copy']:
                course_places = (course.all_place)

            if course.__class__.__name__ == 'LifeCourse':
                type_place = 'place_offline'
                type_course = 'life'

            if course.__class__.__name__ == 'OnlineCourse':
                type_place = 'place_online'
                type_course = 'online'

        return '200 OK', render('copy_course.html', item=course, objects_list=site.categories,
                                places=course_places, type_place=type_place, type_course=type_course)
