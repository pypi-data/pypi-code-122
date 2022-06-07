# import sys
#
# import cv2
# import numpy as np
#
#
# def remove_grid_lines(src):
#     clean_lines_h = remove_lines(src, np.ones((1, 10), np.uint8), np.ones((1, 10), np.uint8))
#     clean_lines_v = remove_lines(src, np.ones((10, 1), np.uint8), np.ones((10, 1), np.uint8))
#     return src - clean_lines_h - clean_lines_v
#
#
# def remove_lines(src, kernel1, kernel2):
#     src = cv2.bitwise_not(src)
#     dilation = cv2.bitwise_not(cv2.dilate(cv2.erode(src, kernel1, iterations=1), kernel1, iterations=1))
#     clean_lines = cv2.dilate(cv2.erode(dilation, kernel2, iterations=6), kernel2, iterations=6)
#     return clean_lines
#
#
# def main(argv):
#     # cv2.namedWindow("Out")
#
#     original_image = cv2.resize(cv2.imread(argv[0]), (640, 640))
#     original_image = cv2.GaussianBlur(cv2.medianBlur(original_image, 3), (3, 3), 0)
#     hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
#
#     binary_image = cv2.inRange(hsv_image, (6, 120, 150), (20, 255, 255))
#
#     binary_image = remove_grid_lines(binary_image)
#
#     # binary_image = cv2.GaussianBlur(cv2.medianBlur(binary_image, 3), (3, 3), 0)
#     binary_image = cv2.GaussianBlur(binary_image, (3, 3), 0)
#
#     binary_image = cv2.morphologyEx(
#         binary_image, cv2.MORPH_CLOSE,
#         np.array(
#             [[0, 0, 0, 1, 1],
#              [0, 0, 1, 1, 1],
#              [0, 1, 1, 1, 0],
#              [1, 1, 1, 0, 0],
#              [1, 1, 0, 0, 0]],
#             dtype=np.uint8
#         ),
#         # cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
#         iterations=5
#     )
#
#     # print(cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)))
#
#     # binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
#     _, binary_image = cv2.threshold(binary_image, 120, 255, cv2.THRESH_BINARY)
#
#     nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
#     sizes = stats[1:, -1]
#     nb_components = nb_components - 1
#     min_size = 300
#     bw = np.zeros(output.shape, np.uint8)
#     for i in range(0, nb_components):
#         if sizes[i] >= min_size:
#             bw[output == i + 1] = 255
#
#     binary_image = bw
#
#     binary_image = cv2.dilate(binary_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=15)
#     binary_image = cv2.erode(binary_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=15)
#
#     contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#
#     c = max(contours, key=cv2.contourArea)
#     print(f"Area = {(cv2.contourArea(c) * 8 * 8 / (640 * 640))}")
#
#     out = np.zeros_like(bw)
#     cv2.drawContours(out, [c], -1, 255, cv2.FILLED)
#
#     # cv2.imwrite("HSV.jpg", hsv_image)
#     # cv2.imwrite("clean.jpg", binary_image)
#     # cv2.imwrite("out.jpg", out)
#     cv2.imshow("out.jpg", out)
#
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     main(sys.argv[1:])
