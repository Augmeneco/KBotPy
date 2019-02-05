from ruamel import yaml
import inspect
import time
from datetime import datetime


def imported_from():
    inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0])[0].split('/')
    return


def log_print(text, type):
    print('[' + datetime.now().strftime("%H:%M:%S") + '] '+text)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        #else:
        #    cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class KBEvent(object):

    def __init__(self):
        self.__handlers = []

    def add(self, handler):
        self.__handlers.append(handler)
        #return self

    def remove(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(self, *args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler


class KBot(metaclass=Singleton):
    SETTINGS = yaml.safe_load(open('./configs/settings.yml').read())

    onMessage = KBEvent()
    onOnline = KBEvent()
    onOffline = KBEvent()