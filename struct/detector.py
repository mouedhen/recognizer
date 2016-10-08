# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Detector(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def detect(self, source):
        pass
