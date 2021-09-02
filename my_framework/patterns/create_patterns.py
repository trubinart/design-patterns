import copy
import os
from abc import ABC, abstractmethod

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
    def __init__(self, name):
        self.name = name
        self.category = []
        self.all_main_category.append(self)
        self.all_main_category_name.append(name)

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
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

    def clone(self):
        return copy.deepcopy(self)


class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class LifeCourse(Course):
    all_place = {'office_1': 'Офис в центре', 'office_2': 'Офис в химках'}

    def __init__(self, name, category, place):
        super().__init__(name, category)
        self.place = self.all_place[place]
        self.types = 'Курс в Москве'


class OnlineCourse(Course):
    all_place = {'gm': 'Google Meet', 'zoom': 'Zoom'}

    def __init__(self, name, category, place):
        super().__init__(name, category)
        self.place = self.all_place[place]
        self.types = 'Онлайн курс'


class CourseFactory:
    types = {
        'life': LifeCourse,
        'online': OnlineCourse
    }

    @classmethod
    def create(cls, type_, name, category, place):
        return cls.types[type_](name, category, place)


class Engine:
    def __init__(self):
        self.categories = []
        self.courses = []

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
    def create_course(type_, name, category, place):
        return CourseFactory.create(type_, name, category, place)


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


class Logger(metaclass=SingletonByName):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def __init__(self, name):
        self.name = name

    def write(self, text):
        with open(f'{self.path}/log/{self.name}.txt', "a", encoding='utf-8') as f:
            f.write(f'\n{text}')


if __name__ == '__main__':
    a = MainCategory('Web')
    b = Category('Java', '123')
    a.add(b)
    print(b.parent.name, b.name)

    c = MainCategory('Mob')
    d = Category('Java', '123')
    c.add(d)
    print(c.all_main_category)

