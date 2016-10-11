# -*- coding: utf-8 -*-
import cv2


def draw_rectangles(image, rectangles, color):
    for x1, y1, x2, y2 in rectangles:
        cv2.rectangle(image, (x1, y2), (x2, y1), color, 2)
