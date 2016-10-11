#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import cv2
import os
import numpy as np

from dataset import FacesDataSet
from preprocessor import ImagePreprocessor
from detector import HaarDetector
from helpers import draw_rectangles, gif_to_jpeg


DATASET = "/home/chams/data/recognizer/data"
MAXDATA = 100
HAARCASCADEPATH = "/home/chams/data/recognizer/haar_classifier/haarcascade_frontalface_default.xml"


# @TODO : add support of all images' formats
def dir_trainer(args):
    raw_data_path = args.path
    detector = HaarDetector(HAARCASCADEPATH)
    dataset = FacesDataSet(DATASET)

    subjects = map(lambda x: os.path.join(raw_data_path, x), os.listdir(raw_data_path))
    subjects = filter(lambda x: os.path.isdir(x), subjects)
    if not len(subjects) > 0:
        return -1
    for subject in subjects:
        key = os.path.basename(os.path.normpath(subject))
        dataset.init_subject(key)
        images = map(lambda x: os.path.join(subject, x), os.listdir(subject))

        for image in images:
            frame = gif_to_jpeg(image)
            train(detector, dataset, frame, key, reevaluate=False)
            cv2.imshow("Training", frame)
            cv2.waitKey(50)
        print "subject {} training complete".format(key)
    return 0


def video_trainer(args):

    """
    Add faces data of the subject in front of the camera to the dataset
    :param args: must contain the subject ID
    :return: 0 if success
    """

    subject = args.subject
    detector = HaarDetector(HAARCASCADEPATH)
    dataset = FacesDataSet(DATASET)
    capture = cv2.VideoCapture()
    dataset.init_subject(subject)
    capture.open(0)
    while True:
        ret, frame = capture.read()
        total_faces = train(detector, dataset, frame, subject)
        cv2.imshow(subject, frame)
        if total_faces >= MAXDATA:
            print "Training of the subject {} complete. You can quit.".format(subject)
        if 0xFF & cv2.waitKey(5) == 27:
            break
    return 0


def train(detector, dataset, frame, subject, reevaluate=True):

    """
    :param detector: a haar cascade detector
    :param dataset: the dataset where the subject will be added
    :param frame: an opencv image matrix
    :param subject: subject to be added / updated in the dataset
    :param reevaluate: Reevaluate detected face, default True
    :return: Total data images for the subject
    """

    image = ImagePreprocessor.transform(frame)
    rectangles = detector.detect(image)
    draw_rectangles(frame, rectangles, (0, 255, 0))
    total_faces = dataset.subject_data_length(subject)
    if len(rectangles) > 0 and total_faces < MAXDATA:
        for r in rectangles:
            face = ImagePreprocessor.resize(ImagePreprocessor.crop(image, r), (50, 50))
            if reevaluate:
                if len(detector.detect(face)) == 1:
                    dataset.add(subject, face)
            else:
                dataset.add(subject, face)
    return total_faces


def dir_recognizer(args):
    print 'directory recognizer'
    return 0


def video_recognizer(args):
    print 'video trainer'
    return 0


DESCRIPTION = "Real time facial recognition and identification with OpenCV and Python"
VIDEO_TRAINER = "Add new subject or update old subject from video source"
DIR_TRAINER = "Add new subjects or update old to the data set  from a directory. The directory structure must be " \
              "dir/subject1_id dir/subject2_id ..."
VIDEO_RECOGNIZER = "Identify the subjects in front of camera"
DIR_RECOGNIZER = "Identify the subjects in all images in the specified directory and subdirectory"


def __main__():

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    sub_parser = parser.add_subparsers()

    parser_video_trainer = sub_parser.add_parser('video_trainer', help=VIDEO_TRAINER)
    parser_video_trainer.add_argument('--subject', '-s', help='Subject identifier', required=True)
    parser_video_trainer.set_defaults(func=video_trainer)

    parser_dir_trainer = sub_parser.add_parser('dir_trainer', help=DIR_TRAINER)
    parser_dir_trainer.add_argument('--path', '-p', help='Data directory path', required=True)
    parser_dir_trainer.set_defaults(func=dir_trainer)

    parser_video_recognizer = sub_parser.add_parser('video_recognizer', help=VIDEO_RECOGNIZER)
    parser_video_recognizer.set_defaults(func=video_recognizer)

    parser_dir_recognizer = sub_parser.add_parser('dir_recognizer', help=DIR_RECOGNIZER)
    parser_dir_recognizer.add_argument('--path', '-p', help='Data directory path', required=True)
    parser_dir_recognizer.set_defaults(func=dir_recognizer)

    # return the appropriate function with args
    args = parser.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(__main__())
