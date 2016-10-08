# -*- coding: utf-8 -*-
import sys
import cv2
from struct.preprocessor import Preprocessor


sys.path.append("..")


class ImagePreprocessor(Preprocessor):

    def __init__(self):
        pass

    def transform(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(image)

    def compute(self, images):
        return super(ImagePreprocessor, self).compute(images)
