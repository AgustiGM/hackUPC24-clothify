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

winStride = (8, 8)
padding = (8, 8)
locations = ((10, 20),)
mat = []
shape = (199, 3, 1764)
arr = np.empty(shape)
featureList = []

for index, imdir in enumerate(os.listdir(directory)):
    images = []
    for image in os.listdir(f'{directory}{imdir}'):
        im = cv2.imread(f'{directory}{imdir}{os.sep}{image}')
        down_width = 128
        down_height = 128
        down_points = (down_width, down_height)
        resized = cv2.resize(im, down_points)
        hist = hog.compute(resized, winStride, padding, locations)
        images.append(hist)
    featureList.append(images);
    if index % 10 == 0:
        print(f'Iteration:{index}')

labels = []
data = []
for i, image_set in enumerate(featureList):
    for concrete_image in image_set:
        labels.append(i)
        data.append(concrete_image)

arr = np.array(data)
list_of_tuples = list(zip(data, labels))
pd = pandas.DataFrame(list_of_tuples, columns=['features', 'labels'])
pd.to_csv('dataframe2.csv')

# arr = np.array(data)
#
# np.save('num.py', arr)
