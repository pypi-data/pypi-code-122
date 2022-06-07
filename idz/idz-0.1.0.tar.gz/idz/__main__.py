# import sys
#
# import cv2
# import numpy as np
#
#
# def show_wait_destroy(window_name, image):
#     cv2.imshow(window_name, image)
#     cv2.moveWindow(window_name, 500, 0)
#     cv2.waitKey(0)
#     cv2.destroyWindow(window_name)
#
#
# def main(argv):
#     image = cv2.resize(cv2.imread(argv[0]), (640, 640))
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     gray = cv2.GaussianBlur(gray, (3, 3), 0)
#
#     show_wait_destroy("gray", gray)
#
#     kernel_clean = np.ones((2, 2), np.uint8)
#     gray = cv2.erode(gray, kernel_clean, iterations=1)
#     gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))
#
#     show_wait_destroy("preprocess", gray)
#
#     kernel_horizontal = np.ones((1, 70), np.uint8)
#     morphed_horizontal = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel_horizontal)
#     gray = cv2.add(gray, (255 - morphed_horizontal))
#
#     show_wait_destroy("horizontal", gray)
#
#     kernel_vertical = np.ones((70, 1), np.uint8)
#     morphed_vertical = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel_vertical)
#     gray = cv2.add(gray, (255 - morphed_vertical))
#
#     show_wait_destroy("vertical", gray)
#
#     gray = cv2.GaussianBlur(gray, (5, 5), 0)
#     gray = cv2.bitwise_not(gray)
#     # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
#     thresh, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#
#
#
#     gray = cv2.GaussianBlur(gray, (5, 5), 0)
#     kernel_clean = np.ones((5, 5), np.uint8)
#     gray = cv2.erode(gray, kernel_clean, iterations=1)
#     gray = cv2.dilate(gray, kernel_clean, iterations=1)
#
#     show_wait_destroy("postprocess", gray)
#
#     # contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     # cv2.drawContours(gray, contours, -1, (0, 255, 0), 3)
#
#     show_wait_destroy("result", gray)
#     # show_wait_destroy("mask", mask)
#
#
# if __name__ == "__main__":
#     main(sys.argv[1:])


import sys

import cv2
import numpy as np


def show_wait_destroy(window_name, image):
    cv2.imshow(window_name, image)
    cv2.moveWindow(window_name, 500, 0)
    cv2.waitKey(0)
    cv2.destroyWindow(window_name)


def main(argv):
    image = cv2.resize(cv2.imread(argv[0]), (640, 640))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    show_wait_destroy("gray", gray)

    gray = cv2.bitwise_not(gray)

    thresh, gray = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel_clean = np.ones((2, 2), np.uint8)
    gray = cv2.erode(gray, kernel_clean, iterations=1)
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))

    show_wait_destroy("preprocess", gray)

    kernel_horizontal = np.ones((1, 70), np.uint8)
    morphed_horizontal = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel_horizontal)
    gray = cv2.add(gray, (255 - morphed_horizontal))

    show_wait_destroy("horizontal", gray)

    kernel_vertical = np.ones((70, 1), np.uint8)
    morphed_vertical = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel_vertical)
    gray = cv2.add(gray, (255 - morphed_vertical))

    show_wait_destroy("vertical", gray)

    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.bitwise_not(gray)
    # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    # thresh, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    kernel_clean = np.ones((5, 5), np.uint8)
    gray = cv2.erode(gray, kernel_clean, iterations=1)
    gray = cv2.dilate(gray, kernel_clean, iterations=1)
    show_wait_destroy("postprocess", gray)

    edges = cv2.Canny(gray, 10, 255)
    show_wait_destroy("canny_edges", edges)
    # show_wait_destroy("postprocess", gray)

    # contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(gray, contours, -1, (0, 255, 0), 3)

    show_wait_destroy("result", gray)
    # show_wait_destroy("mask", mask)


if __name__ == "__main__":
    main(sys.argv[1:])
