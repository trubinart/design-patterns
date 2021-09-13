import sqlite3
import threading
from .db_data_mapper import MainCategoryMapper, CategoryMapper, CourseMapper,\
    StudentMapper, RegistrationMapper

connection = sqlite3.connect('./scgool_db.sqlite')

class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, MainCategoryModel):
            return MainCategoryMapper(connection)
        elif isinstance(obj, CategoryModel):
            return CategoryMapper(connection)
        elif isinstance(obj, CourseModel):
            return CourseMapper(connection)
        elif isinstance(obj, StudentModel):
            return StudentMapper(connection)
        elif isinstance(obj, RegistrarionModel):
            return RegistrationMapper(connection)


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            print(obj)
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class MainCategoryModel(DomainObject):
    def __init__(self, name):
        self.name = name

class CategoryModel(DomainObject):
    def __init__(self, name, id_main_category):
        self.name = name
        self.id_main_category = id_main_category

class CourseModel(DomainObject):
    def __init__(self, name, course_type, id_category, places):
        self.name = name
        self.course_type = course_type
        self.id_category = id_category
        self.places = places

class StudentModel(DomainObject):
    def __init__(self, name, phone, email):
        self.name = name
        self.id = id
        self.phone = phone
        self.email = email

class RegistrarionModel(DomainObject):
    def __init__(self, id_course, id_student):
        self.id_course = id_course
        self.id_student = id_student




