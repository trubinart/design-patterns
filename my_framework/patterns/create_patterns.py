import copy
import os
from abc import ABC
from .behavioral_patterns import SubscribeCourse, ProtoSubscriber


class MainCategoryPrototype(ABC):
    all_main_category = []
    all_main_category_name = []

    def set_parent(self, parent):
        self.parent = parent

    def get_main_gategory(self, name):
        for i in self.all_main_category:
            if i.name == name:
                return i


class MainCategory(MainCategoryPrototype):
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.category = []


    def add(self, category):
        self.category.append(category)
        category.set_parent(self)

    def remove(self, category):
        self.category.remove(category)
        category.set_parent(None)


class Category(MainCategoryPrototype):
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.id = category

    def clone(self):
        return copy.deepcopy(self)



class CoursePrototype:

    all_students = []

    def clone(self):
        return copy.deepcopy(self)

    @property
    def get_iter(self):
        return iter(self.all_students)


class Course(CoursePrototype, SubscribeCourse):

    def __init__(self, name, category, main_category):
        self.name = name
        self.category = category
        self.main_category = main_category


class LifeCourse(Course):
    # all_place = {'office_1': 'Офис в центре', 'office_2': 'Офис в химках'}

    def __init__(self, name, category, place, main_category):
        super().__init__(name, category, main_category)
        self.place = place
        self.types = 'Курс в Москве'



class OnlineCourse(Course):
    # all_place = {'gm': 'Google Meet', 'zoom': 'Zoom'}

    def __init__(self, name, category, place, main_category):
        super().__init__(name, category, main_category)
        self.place = place
        self.types = 'Онлайн курс'



class CourseFactory:
    types = {
        'Офлайн формат': LifeCourse,
        'Онлайн формат': OnlineCourse
    }

    @classmethod
    def create(cls, type_, name, category, place, main_category):
        return cls.types[type_](name, category, place, main_category)


class Engine:
    def __init__(self):
        self.categories = []
        self.courses = []
        self.students = []

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    @staticmethod
    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category, place, main_category):
        return CourseFactory.create(type_, name, category, place, main_category)


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


# class Logger(metaclass=SingletonByName):
#     path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
#     def __init__(self, name):
#         self.name = name
#
#     def write(self, text):
#         with open(f'{self.path}/log/{self.name}.txt', "a", encoding='utf-8') as f:
#             f.write(f'\n{text}')


class User:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email


class Student(User, ProtoSubscriber):

    def __init__(self, name, phone, email):
        self.courses = []
        super().__init__(name, phone, email)

    def update(self, course: Course):
        for key, value in self.notify_type.items():
            if value == True:
                print(f'Уведомили {self.name} по {key} об обновлении курса {course.name}')


