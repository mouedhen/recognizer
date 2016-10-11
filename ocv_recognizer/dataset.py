# -*- coding: utf-8 -*-
import os
import cv2
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


class FacesDataSet(DataSet):

    def __init__(self, path):
        if not os.path.isdir(path):
            try:
                os.mkdir(path)
            except OSError:
                raise OSError
        self.path = path
        self.keys = []
        self.values = []

    def init_subject(self, key):
        subject = os.path.join(self.path, key)
        if not os.path.isdir(subject):
            os.mkdir(subject)

    def get_by_key(self, key):
        subject_path = os.path.join(self.path, key)
        if not os.path.isdir(subject_path):
            return []
        faces = os.listdir(subject_path)
        return map(lambda x: os.path.join(subject_path, x), faces)

    def get(self):
        subjects = os.listdir(self.path)
        if not subjects:
            return self.values, self.keys
        subjects = filter(lambda x: os.path.isdir(os.path.join(self.path, x)), subjects)
        for subject in subjects:
            self.values.append(map(lambda x: os.path.join(subjects, x), os.listdir(subject)))
            self.keys.append(os.path.basename(os.path.normpath(subject)))
        return self.values, self.keys

    def length(self):
        if not self.values:
            self.get()
        return len(self.values)

    def total_subject(self):
        if not self.keys:
            self.get()
        return len(set(self.keys))

    def subject_data_length(self, keys):
        return len(
            os.listdir(
                os.path.join(self.path, keys)
            )
        )

    def add(self, subject, image):
        subject_path = os.path.join(self.path, subject)
        if not os.path.isdir(subject_path):
            try:
                os.mkdir(subject_path)
            except OSError:
                raise OSError
        cv2.imwrite(
            os.path.join(subject_path, str(self.auto_increment(subject)) + ".jpg"),
            image,
            [int(cv2.IMWRITE_JPEG_OPTIMIZE), 100]
        )

    def auto_increment(self, key):
        subject_data = self.get_by_key(key)
        if len(subject_data) > 0:
            data_id = map(lambda x: int(os.path.basename(os.path.normpath(x)).split('.')[0]), subject_data)
            data_id.sort(reverse=True)
            return data_id[0] + 1
        else:
            return 0
