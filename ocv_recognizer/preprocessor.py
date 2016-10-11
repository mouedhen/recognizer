# -*- coding: utf-8 -*-
import cv2
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


class ImagePreprocessor(Preprocessor):

    def __init__(self):
        pass

    @staticmethod
    def transform(image):
        return cv2.equalizeHist(
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        )

    @staticmethod
    def crop(image, rectangle):
        x1, y1, x2, y2 = rectangle
        return image[y1:y2, x1:x2]

    @staticmethod
    def resize(image, dimension=(100, 100)):
        return cv2.resize(image, dimension, interpolation=cv2.INTER_CUBIC)

    def compute(self, images):
        return super(ImagePreprocessor, self).compute(images)
