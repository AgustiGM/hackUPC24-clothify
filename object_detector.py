import os
import numpy as np

import cv2


def get_sobel_edges(image, ddepth=cv2.CV_16S):
    grad_x = cv2.Sobel(image, ddepth, 1, 0, ksize=5)
    grad_y = cv2.Sobel(image, ddepth, 0, 1, ksize=5)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad


def extract_important_object(image, kernel=(25, 25), initial_resize=(500, 500)):
    res_image = cv2.resize(image, initial_resize)
    gray_image = cv2.cvtColor(res_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, kernel, 0)
    grad = get_sobel_edges(blurred_image)
    diff_th, otsu_image = cv2.threshold(grad, np.amin(blurred_image), np.amax(blurred_image),
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    closing = cv2.morphologyEx(otsu_image, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = []
    # TODO: Fix the cutrest
    for contour in contours:
        if len(contour) > len(largest):
            largest = contour
    x, y, w, h = cv2.boundingRect(largest)
    return res_image[x:x + w, y:y + h]

#
# path = f'images{os.sep}4{os.sep}image0.jpg'
#
# image = cv2.imread(path)
#
# cropped = extract_important_object(image)
#
# cv2.imshow('cropped', cropped)
# cv2.imshow('original', cv2.resize(image, (500, 500)))
#
# cv2.waitKey(0)

cv2.destroyAllWindows()
