#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import cv2

from dataset import FacesDataSet
from preprocessor import ImagePreprocessor
from detector import HaarDetector
from helpers import draw_rectangles


DATASET = "/home/chams/data/recognizer/data"
MAXDATA = 100
HAARCASCADEPATH = "/home/chams/data/recognizer/haar_classifier/haarcascade_frontalface_default.xml"


def dir_train(args):
    print 'directory trainer'
    return 0


def video_trainer(args):
    # Initialize
    subject = args.subject
    detector = HaarDetector(HAARCASCADEPATH)
    dataset = FacesDataSet(DATASET)
    capture = cv2.VideoCapture()

    dataset.init_subject(subject)
    capture.open(0)
    while True:
        # capture video frame by frame
        ret, frame = capture.read()
        # preprocess frame
        image = ImagePreprocessor.transform(frame)
        # detect faces
        rectangles = detector.detect(image)
        # Draw rectangle in the frame that will be shown
        draw_rectangles(frame, rectangles, (0, 255, 0))

        total_faces = dataset.subject_data_length(subject)

        print "subject face number {}".format(total_faces)

        if len(rectangles) > 0 and total_faces < MAXDATA:
            for r in rectangles:
                # crop and resize image
                face = ImagePreprocessor.resize(ImagePreprocessor.crop(image, r))
                if len(detector.detect(face)) == 1:
                    # add the image to the dataset
                    dataset.add(subject, face)

        cv2.imshow(subject, frame)
        if total_faces >= MAXDATA:
            print "Training of the subject {} complete. You can quit.".format(subject)
        if 0xFF & cv2.waitKey(5) == 27:
            break
    return 0


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
    parser_dir_trainer.set_defaults(func=dir_train)

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
