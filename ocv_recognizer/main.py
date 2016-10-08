#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys


def video_train(args):
    print 'video trainer'
    return 0


def dir_train(args):
    print 'directory trainer'
    return 0


def video_recognizer(args):
    print 'video recognizer'
    return 0


def dir_recognizer(args):
    print 'directory recognizer'
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
    parser_video_trainer.set_defaults(func=video_train)

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
