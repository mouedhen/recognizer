# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from preprocessor import ImagePreprocessor
from abc import ABCMeta, abstractmethod


class Detector(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def detect(self, source):
        pass


class HaarDetector(Detector):

    def __init__(self, cascade_path, scale_factor=1.2, min_neighbors=5, min_size=(30, 30)):
        if not os.path.isfile(cascade_path):
            raise EOFError("[ERROR] The haar cascade file {} do not exist".format(cascade_path))
        self.cascade = cv2.CascadeClassifier(cascade_path)
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    def detect(self, src):
        src = ImagePreprocessor.transform(src)
        rectangles = self.cascade.detectMultiScale(src, scaleFactor=self.scale_factor,
                                                   minNeighbors=self.min_neighbors, minSize=self.min_size)
        if len(rectangles) == 0:
            return np.ndarray((0,))
        rectangles[:, 2:] += rectangles[:, :2]
        return rectangles
