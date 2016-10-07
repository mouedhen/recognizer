from abc import ABCMeta, abstractmethod


class Preprocessor(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __transform(self, xi):
        pass

    def compute(self, x):
        xt = []
        for xi in x:
            xt.append(self.__transform(xi))
        return xt
