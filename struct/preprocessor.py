from abc import ABCMeta, abstractmethod


class Preprocessor(object):

    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def transform(xi):
        pass

    def compute(self, x):
        xt = []
        for xi in x:
            xt.append(self.transform(xi))
        return xt
