import sys
from dataclasses import dataclass
from functools import partial

import cv2
import numpy as np


@dataclass
class Channel:
    name: str
    lower_bound: int
    upper_bound: int


class Window:
    def __init__(self, image, name: str, channels: list[Channel], min_suffix: str = " min", max_suffix: str = " max"):
        self.__name = name
        # self.mask
        self.__original_image = image.copy()
        self.__converted = self.__prepare_image()
        self.__channels = channels
        self.__min_suffix = min_suffix
        self.__max_suffix = max_suffix

    def __prepare_image(self):
        resized = cv2.resize(self.__original_image, (640, 640))
        blured = cv2.GaussianBlur(cv2.medianBlur(resized, 3), (3, 3), 0)
        return cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)

    def __init_window(self):
        cv2.namedWindow(self.__name)
        for i, channel in enumerate(self.__channels):
            cv2.createTrackbar(channel.name + self.__min_suffix, self.__name, channel.lower_bound, channel.upper_bound,
                               partial(self.__update_lower_bound, i))
            cv2.createTrackbar(channel.name + self.__max_suffix, self.__name, channel.upper_bound, channel.upper_bound,
                               partial(self.__update_upper_bound, i))
        self.__update()

    def __update(self):
        print(np.array([x.lower_bound for x in self.__channels], dtype=np.uint8),
              np.array([x.upper_bound for x in self.__channels], dtype=np.uint8))

        binary_image = cv2.inRange(self.__converted,
                                   np.array([x.lower_bound for x in self.__channels], dtype=np.uint8),
                                   np.array([x.upper_bound for x in self.__channels], dtype=np.uint8))
        binary_image = remove_grid_lines(binary_image)
        binary_image = cv2.GaussianBlur(binary_image, (3, 3), 0)
        binary_image = cv2.morphologyEx(
            binary_image, cv2.MORPH_CLOSE,
            np.array(
                [[0, 0, 0, 1, 1],
                 [0, 0, 1, 1, 1],
                 [0, 1, 1, 1, 0],
                 [1, 1, 1, 0, 0],
                 [1, 1, 0, 0, 0]],
                dtype=np.uint8
            ),
            iterations=5
        )

        _, binary_image = cv2.threshold(binary_image, 120, 255, cv2.THRESH_BINARY)

        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
        sizes = stats[1:, -1]
        nb_components = nb_components - 1
        min_size = 300
        bw = np.zeros(output.shape, np.uint8)
        for i in range(0, nb_components):
            if sizes[i] >= min_size:
                bw[output == i + 1] = 255

        binary_image = bw

        binary_image = cv2.dilate(binary_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=15)
        binary_image = cv2.erode(binary_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=15)

        contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        out = np.zeros_like(bw)
        if contours:
            c = max(contours, key=cv2.contourArea)
            print(f"Area = {(cv2.contourArea(c) * 8 * 8 / (640 * 640))}")
            cv2.drawContours(out, [c], -1, 255, cv2.FILLED)

        cv2.imshow(self.__name, out)

    def __update_lower_bound(self, channel: int, pos: int):
        self.__channels[channel].lower_bound = pos
        self.__update()

    def __update_upper_bound(self, channel: int, pos: int):
        self.__channels[channel].upper_bound = pos
        self.__update()

    def run(self):
        self.__init_window()
        while True:
            print("Press [q] to close the window.")
            k = cv2.waitKey()
            if k == ord("q"):
                cv2.destroyWindow(self.__name)
                break
        cv2.destroyAllWindows()


def remove_grid_lines(src):
    clean_lines_h = remove_lines(src, np.ones((1, 10), np.uint8), np.ones((1, 10), np.uint8))
    clean_lines_v = remove_lines(src, np.ones((10, 1), np.uint8), np.ones((10, 1), np.uint8))
    return src - clean_lines_h - clean_lines_v


def remove_lines(src, kernel1, kernel2):
    src = cv2.bitwise_not(src)
    dilation = cv2.bitwise_not(cv2.dilate(cv2.erode(src, kernel1, iterations=1), kernel1, iterations=1))
    clean_lines = cv2.dilate(cv2.erode(dilation, kernel2, iterations=6), kernel2, iterations=6)
    return clean_lines


if __name__ == "__main__":
    Window(cv2.imread(sys.argv[1]), "qwe", [Channel("H", 0, 180), Channel("S", 0, 255), Channel("V", 0, 255)]).run()
