from abc import ABCMeta, abstractmethod


class Feature(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def compute(self, x, y):
        pass

    @abstractmethod
    def extract(self, x):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass
