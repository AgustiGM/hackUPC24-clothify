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


def extract_important_object(image, kernel=(25, 25), initial_resize=(500, 500), show_images=False):
    res_image = cv2.resize(image, initial_resize)
    gray_image = cv2.cvtColor(res_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, kernel, 0)
    grad = get_sobel_edges(blurred_image)
    cv2.imshow('sobel', grad)
    diff_th, otsu_image = cv2.threshold(grad, np.amin(blurred_image), np.amax(blurred_image),
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    closing = cv2.morphologyEx(otsu_image, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_c = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
    largest = []
    # TODO: Fix the cutrest
    for contour in contours:
        if len(contour) > len(largest):
            largest = contour
    x, y, w, h = cv2.boundingRect(largest)
    if show_images:
        cv2.drawContours(res_image, contours, -1, (0, 0, 255), 3)
        cv2.rectangle(res_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('contour', res_image)
    if len(sorted_c) > 1 and len(sorted_c[0])*0.8 < len(sorted_c[1]):
        return res_image
    return res_image[y:y+h, x:x+w]

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

# cv2.destroyAllWindows()
