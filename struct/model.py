from abc import ABCMeta, abstractmethod

from feature import Feature
from classifer import Classifier


class Model(object):

    __metaclass__ = ABCMeta

    def __init__(self, feature, classifier):

        if not isinstance(feature, Feature):
            raise TypeError("feature must be type of Feature")
        if not isinstance(classifier, Classifier):
                raise TypeError("classifier must be type of Classifier")

        self.feature = feature
        self.classifier = classifier

    def compute(self, x, y):
        features = self.feature.compute(x, y)
        self.classifier.compute(features, y)

    def predict(self, x):
        subject = self.feature.extract(x)
        return self.classifier.predict(subject)
