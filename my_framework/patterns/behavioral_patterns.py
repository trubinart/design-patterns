from abc import ABC, abstractmethod
import jsonpickle
import json
import os


class ProtoSubscribeCourse(ABC):

    @abstractmethod
    def add_subscriber(self, subscriber):
        pass

    @abstractmethod
    def del_subscriber(self, subscriber):
        pass

    @abstractmethod
    def notify(self):
        pass


class SubscribeCourse(ProtoSubscribeCourse):
    _subscribers = []

    def add_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def del_subscriber(self, subscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for item in self._subscribers:
            item.update(self)


class ProtoSubscriber(ABC):
    notify_type = {'sms': True, 'email': True}

    @abstractmethod
    def update(self, course: SubscribeCourse):
        pass


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def give_data(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def take_data(data):
        return jsonpickle.loads(data)


class LoggerProto(ABC):

    @abstractmethod
    def write(self, text):
        pass


class ConsoleLogger(LoggerProto):

    def __init__(self, name):
        self.name = name

    def write(self, text):
        print(text)


class FileWritter(LoggerProto):

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, name):
        self.name = name

    def write(self, text):
        with open(f'{self.path}/log/{self.name}.txt', "a", encoding='utf-8') as f:
            f.write(f'\n{text}')


class Logger:
    def __init__(self, name, console=None, file=None):
        self.name = name

        if console:
            self.console = ConsoleLogger(self.name)

        if file:
            self.file = FileWritter(self.name)

    def write(self, text):
        if self.console:
            self.console.write(text)

        if self.file:
            self.file.write(text)
