import sqlite3
from .create_patterns import Engine, MainCategory, Student

connection = sqlite3.connect('./scgool_db.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class MainCategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'main_category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            main_categiry = MainCategory(name)
            main_categiry.id = id
            result.append(main_categiry)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        id_1, name = self.cursor.fetchone()
        if name:
            return MainCategory(name, id_1)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, name):
        statement = f"SELECT id, name FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        id_cat, name_cat = self.cursor.fetchone()
        if name:
            return MainCategory(name_cat, id_cat)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        print(obj.name)
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self, engine):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, id_main_category = item
            main_category = engine.create_category(name, id_main_category)
            main_category.id = id
            result.append(main_category)
        return result

    def find_by_id(self, engine, id):
        statement = f"SELECT id, name, id_main_category FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        id, name, id_main_category = self.cursor.fetchone()
        if name:
            return engine.create_category(name, id_main_category)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, engine, name):
        statement = f"SELECT id, name FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        id_cat, name_cat, id_main_category_cat = self.cursor.fetchone()
        if name:
            return engine.create_category(name_cat, id_main_category_cat)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, id_main_category) VALUES (?,?)"
        self.cursor.execute(statement, (obj.name, obj.id_main_category))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


class CourseMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'courses'

    def all(self, engine):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, course_type, id_category, places = item
            category_object = CategoryMapper(connection)
            category = category_object.find_by_id(engine, id_category)
            main_category_object = MainCategoryMapper(connection)
            main_category = main_category_object.find_by_id(category.id).name
            course = engine.create_course(course_type, name, category.name, places, main_category)
            course.id = id
            result.append(course)
        return result

    def find_by_id(self, engine, id):
        statement = f"SELECT id, name, course_type, id_category, places FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        id, name, course_type, id_category, places = self.cursor.fetchone()
        if name:
            category_object = CategoryMapper(connection)
            category = category_object.find_by_id(engine, id_category)
            main_category_object = MainCategoryMapper(connection)
            main_category = main_category_object.find_by_id(category.id).name
            return engine.create_course(course_type, name, category.name, places, main_category)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, engine, name):
        statement = f"SELECT id, name FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        id, name_cor, course_type, id_category, places = self.cursor.fetchone()
        if name:
            return engine.create_course(course_type, name_cor, id_category, places)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, course_type, id_category, places) VALUES (?,?,?,?)"
        self.cursor.execute(statement, (obj.name, obj.course_type, obj.id_category, obj.places))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, id, new_name):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (new_name, id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def copy(self, id):
        statement = f"INSERT INTO {self.tablename} (name, course_type, id_category, places) SELECT name, course_type, id_category, places FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id))
        print(self.cursor.fetchone())
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'students'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, phone, email = item
            student = Student(name, phone, email)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name, phone, email FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        id, name, phone, email = self.cursor.fetchone()
        if name:
            return Student(name, phone, email)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, phone, email) VALUES (?,?,?)"
        self.cursor.execute(statement, (obj.name, obj.phone, obj.email))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


class RegistrationMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'course_registration'

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (id_course, id_student) VALUES (?,?)"
        self.cursor.execute(statement, (obj.id_course, obj.id_student))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)
