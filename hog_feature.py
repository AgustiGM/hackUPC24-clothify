import os
import cv2
import numpy as np
import pandas

image_directory = f'processed_images{os.sep}'

resized_directory = f'resizedImages{os.sep}'

winSize = (64, 64)
blockSize = (16, 16)
blockStride = (8, 8)
cellSize = (8, 8)
nbins = 9
derivAperture = 1
winSigma = 4.
histogramNormType = 0
L2HysThreshold = 2.0000000000000001e-01
gammaCorrection = 0
nlevels = 64
hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture, winSigma,
                        histogramNormType, L2HysThreshold, gammaCorrection, nlevels)

down_width = 128
down_height = 128
down_points = (down_width, down_height)
winStride = (8, 8)
padding = (8, 8)
locations = ((10, 20),)


def get_hog_feature_vector(image):
    resized = cv2.resize(image, down_points)
    hist = hog.compute(resized, winStride, padding, locations)
    return hist


def transform_images_to_hog_from_root_directory(directory, transform_function=get_hog_feature_vector):
    _labels = []
    _data = []
    _image_route = []
    for index, imdir in enumerate(os.listdir(directory if directory.endswith(os.sep) else directory + os.sep)):
        images = []
        for image in os.listdir(f'{directory}{imdir}'):
            im = cv2.imread(f'{directory}{imdir}{os.sep}{image}')
            images.append(np.array(transform_function(im)))
            _labels.append(imdir)
            _data.append(np.array(transform_function(im)))
            _image_route.append([imdir, image])
        if index % 10 == 0:
            print(f'Iteration:{index}')

    return _data, _labels, _image_route


def aux_func(image):
    return cv2.resize(image, (32, 32)).flatten()


data, labels, image_route = transform_images_to_hog_from_root_directory(image_directory, transform_function=aux_func)

arr = np.array(data)
list_of_tuples = list(zip(data, labels, image_route))
pd = pandas.DataFrame(list_of_tuples, columns=['features', 'labels', 'routes'])
pd.to_pickle('dataframe_images.csv')

# arr = np.array(data)
#
# np.save('num.py', arr)
