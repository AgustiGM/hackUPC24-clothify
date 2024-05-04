import os
import cv2
import numpy as np
import pandas

directory = f'images{os.sep}'

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


mat = []
shape = (199, 3, 1764)
arr = np.empty(shape)
featureList = []

labels = []
data = []
image_route = []
for index, imdir in enumerate(os.listdir(directory)):
    images = []
    for image in os.listdir(f'{directory}{imdir}'):
        im = cv2.imread(f'{directory}{imdir}{os.sep}{image}')
        images.append(np.array(get_hog_feature_vector(im)))
        labels.append(imdir)
        data.append(np.array(get_hog_feature_vector(im)))
        image_route.append([imdir, image])
    featureList.append(images)
    if index % 10 == 0:
        print(f'Iteration:{index}')

# labels = []
# data = []
# image_route = []
# for i, image_set in enumerate(featureList):
#     for j, concrete_image in enumerate(image_set):
#         labels.append(i)
#         image_route.append([i, f'image{j}'])
#         data.append(concrete_image)

arr = np.array(data)
list_of_tuples = list(zip(data, labels, image_route))
pd = pandas.DataFrame(list_of_tuples, columns=['features', 'labels', 'routes'])
pd.to_pickle('dataframe.csv')

# arr = np.array(data)
#
# np.save('num.py', arr)
