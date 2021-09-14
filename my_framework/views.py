from framework.render import render
import datetime
from patterns.create_patterns import Engine, \
    MainCategory, MainCategoryPrototype, Student
from patterns.structure_patterns import AppRoute, Debug
from patterns.behavioral_patterns import BaseSerializer, Logger
from framework.cbv import ListView, CreateView
from patterns.db_data_mapper import MainCategoryMapper, CategoryMapper, \
    CourseMapper, StudentMapper, RegistrationMapper
from patterns.db_unit_of_work import UnitOfWork, MainCategoryModel, \
    CategoryModel, CourseModel, StudentModel, RegistrarionModel
import sqlite3

site = Engine()
main_category = MainCategoryPrototype()
day = datetime.datetime.today().strftime("%d.%m.%Y")

logger = Logger('views', console=True, file=True)
routes = {}

connection = sqlite3.connect('./scgool_db.sqlite')
GetMainCategoryMapper = MainCategoryMapper(connection)
GetCategoryMapper = CategoryMapper(connection)
GetCourseMapper = CourseMapper(connection)
GetStudentMapper = StudentMapper(connection)
GetRegistrationMapper = RegistrationMapper(connection)

try:
    courses_list = GetCourseMapper.all(site)
except:
    courses_list = []

try:
    students_list = GetStudentMapper.all()
except:
    students_list = []


@AppRoute(routes, '/')
class Index(ListView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': courses_list,
                'students_list': students_list}

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
        main_category_name = data['main_category']

        if not name.isdigit() and not main_category_name.isdigit():
            UnitOfWork.new_current()

            try:
                id_main_category = GetMainCategoryMapper.find_by_name(main_category_name).id
            except:
                main_category =  MainCategoryModel(main_category_name)
                main_category.mark_new()
                UnitOfWork.get_current().commit()
                id_main_category = GetMainCategoryMapper.find_by_name(main_category_name).id
            finally:
                category = CategoryModel(name, id_main_category)
                category.mark_new()
                UnitOfWork.get_current().commit()
                print(f'2 = {name}')
                logger.write(f'Создана категория| {name} | и главная категория {main_category_name}')
    @Debug(name='CreateCategory')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/create-course/')
class CreateCourse(CreateView):
    template_name = 'create_course.html'
    queryset = {'category_list': GetCategoryMapper.all(site)}

    def create_obj(self, data):
        name = data['name']
        category_id = data['category_id']
        course_type = data['type']

        if not name.isdigit() and not course_type.isdigit() and category_id.isdigit():
            if course_type == 'Офлайн формат':
                place = data['place_offline']

            elif course_type == 'Онлайн формат':
                place = data['place_online']
            else:
                place = None

            UnitOfWork.new_current()
            course = CourseModel(name, course_type, category_id, place)
            course.mark_new()
            UnitOfWork.get_current().commit()

            logger.write(f'Создан курc| {category_id} | {name} | {course_type} |  {place}')

    @Debug(name='CreateCourse')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/choose-copy-course/')
class ChoseCopyCourse(ListView):
    template_name = 'choose_copy_course.html'
    queryset = {"objects_list": courses_list}

    @Debug(name='ChoseCopyCourse')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/copy-course/')
class CopyCourse(CreateView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': courses_list,
                'students_list': students_list}

    def create_obj(self, data):
        id_course = data['course_for_copy']
        GetCourseMapper.copy(id_course)
        logger.write(f'Курс скопирован | {id_course}')

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

        if not name.isdigit() and not email.isdigit() and phone.isdigit():
            UnitOfWork.new_current()
            student = StudentModel(name, phone, email)
            student.mark_new()
            UnitOfWork.get_current().commit()

            logger.write(f'Студент создан | {name}')

    @Debug(name='CreateStudent')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@AppRoute(routes, '/add-to-cource/')
class AddToCource(CreateView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': courses_list,
                'students_list': students_list, }

    def create_obj(self, data):
        student_id = data['student']
        course_id = data['course']

        UnitOfWork.new_current()
        course = RegistrarionModel(course_id, student_id)
        course.mark_new()
        UnitOfWork.get_current().commit()

        logger.write(f'Студент | {student_id} | записан на курс {course_id}')

    @Debug(name='AddToCource')
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)



@AppRoute(routes, '/correct-course/')
class CorrectCourse(CreateView):
    template_name = 'correct_course.html'
    queryset = {'category_list': GetCategoryMapper.all(site)}

    def create_obj(self, data):
        course_id = data['course']
        course = GetCourseMapper.find_by_id(site,course_id)
        course.id = course_id
        self.queryset['item'] = course

        logger.write(f'Начали редактировать курс | {course_id}')

        @Debug(name='CorrectCourse')
        def __call__(self, *args, **kwargs):
            return super().__call__(*args, **kwargs)


@AppRoute(routes, '/save-correct-course/')
class SaveCorrectCourse(CreateView):
    template_name = 'index.html'
    queryset = {'data': day,
                'courses_list': courses_list,
                'students_list': students_list}

    def create_obj(self, data):
        new_name = data['name']
        course_id = data['course_id']
        GetCourseMapper.update(course_id, new_name)

        logger.write(f'Курс отредактирован | {course_id}')


@AppRoute(routes, '/api/')
class Api:
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).give_data()
