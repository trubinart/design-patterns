from framework.render import render
import datetime
from patterns.create_patterns import Engine, \
    MainCategory, MainCategoryPrototype, Student
from patterns.structure_patterns import AppRoute, Debug
from patterns.behavioral_patterns import BaseSerializer, Logger
from framework.cbv import ListView, CreateView

site = Engine()
main_category = MainCategoryPrototype()
day = datetime.datetime.today().strftime("%d.%m.%Y")

# Создание данных для тестирования
main_category_1 = MainCategory('Главная категория_1')
category_1 = site.create_category('Категория_1', 'id_категории')
category_2 = site.create_category('Категория_2', 'id_категории_2')
category_1.parent = main_category_1
category_2.parent = main_category_1
course_1 = site.create_course('life', 'Название курса', category_1, 'office_1')
course_2 = site.create_course('life', 'Название курса', category_1, 'office_1')
site.categories.append(category_1)
site.categories.append(category_2)
site.courses.append(course_1)
site.courses.append(course_2)
new_student = Student('Артем', 'Телефон', 'Емайл')
site.students.append(new_student)

logger = Logger('views', console=True, file=True)
routes = {}


@AppRoute(routes, '/')
class Index(ListView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': site.courses,
                'students_list': site.students}

    @Debug(name='Index')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, 'no_page')
class NoPage(ListView):
    template_name = '404.html'

    @Debug(name='No_page')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, 'not_access')
class NotAccess(ListView):
    template_name = 'not_access.html'

    @Debug(name='Not_access')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/contacts/')
class Contacts(ListView):
    template_name = 'contacts.html'

    @Debug(name='Contacts')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/create-category/')
class CreateCategory(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data):
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

    @Debug(name='CreateCategory')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/create-course/')
class CreateCourse(CreateView):
    template_name = 'create_course.html'
    queryset = {'category_list': site.categories}

    def create_obj(self, data):
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

    @Debug(name='CreateCourse')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/choose-copy-course/')
class ChoseCopyCourse(ListView):
    template_name = 'choose_copy_course.html'
    queryset = {"objects_list": site.courses}

    @Debug(name='ChoseCopyCourse')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/copy-course/')
class CopyCourse(CreateView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': site.courses,
                'students_list': site.students, }

    def create_obj(self, data):
        name_course = data['course_for_copy']
        new_course = object
        for item in site.courses:
            if item.name == name_course:
                new_course = item.clone()
        site.courses.append(new_course)
        logger.write(f'Курс скопирован | {new_course}')

    @Debug(name='CopyCourse')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/create-student/')
class CreateStudent(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data):
        name = data['fio']
        phone = data['phone']
        email = data['email']
        new_student = Student(name, phone, email)
        site.students.append(new_student)
        logger.write(f'Студент создан | {new_student.name}')

    @Debug(name='CreateStudent')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

@AppRoute(routes, '/add-to-cource/')
class AddToCource(CreateView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': site.courses,
                'students_list': site.students, }

    def create_obj(self, data):
        student_phone = data['student']
        course_name = data['course']

        course = object
        student = object

        for item in site.courses:
            if item.name == course_name:
                course = item

        for item in site.students:
            if item.phone == student_phone:
                student = item

        course.all_students.append(student)
        student.courses.append(course)
        course.add_subscriber(student)
        logger.write(f'Студент | {student.name} | записан на курс {course.name}')

    @Debug(name='AddToCource')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/correct-course/')
class CorrectCourse(CreateView):
    template_name = 'correct_course.html'
    queryset = {'category_list': site.categories}

    def create_obj(self, data):
        course_name = data['course']
        course = object
        for item in site.courses:
            if item.name == course_name:
                course = item

        places = course.all_place
        self.queryset['item'] = course
        self.queryset['places'] = places

        logger.write(f'Начали редактировать курс | {course.name}')

        @Debug(name='CorrectCourse')
        def __call__(self, *args, **kwargs):
            return super().__call__(*args, **kwargs)


@AppRoute(routes, '/save-correct-course/')
class SaveCorrectCourse(CreateView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': site.courses,
                'students_list': site.students}

    def create_obj(self, data):
        parent_course = data['parent_course']
        new_name = data['name']
        new_type_place = data['type_place']
        new_category = data['category_id']

        for item in site.categories:
            if item.name == new_category:
                new_category = item

        for item in site.courses:
            if item.name == parent_course:
                parent_course = item
                parent_course.name = new_name
                parent_course.category = new_category
                parent_course.place = parent_course.all_place[new_type_place]

        parent_course.notify()
        logger.write(f'Курс отредактирован | {parent_course.name}')


@AppRoute(routes, '/api/')
class Api:
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).give_data()
