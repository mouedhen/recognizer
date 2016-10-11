# -*- coding: utf-8 -*-
import cv2
from PIL import Image
import tempfile


def draw_rectangles(image, rectangles, color):
    for x1, y1, x2, y2 in rectangles:
        cv2.rectangle(image, (x1, y2), (x2, y1), color, 2)


def gif_to_jpeg(src):
    img = Image.open(src)

    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        img.save(f.name)
        f.flush()
        out = cv2.imread(f.name)

    assert src is not None and len(src), "Empty"

    return out