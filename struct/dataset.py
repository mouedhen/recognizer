from abc import ABCMeta, abstractmethod


class DataSet(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, key, value):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_by_key(self, key):
        pass

    @abstractmethod
    def length(self):
        pass
