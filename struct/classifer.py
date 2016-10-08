from abc import ABCMeta, abstractmethod


class Classifier(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def compute(self, x, y):
        pass

    @abstractmethod
    def predict(self, x):
        pass

    @abstractmethod
    def update(self, x, y):
        pass
