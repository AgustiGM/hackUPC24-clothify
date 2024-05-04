import cv2
import os
import re

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


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_attributes_from_url(url):
    pattern = r'[0-9]{4}\/[A-Z]\/[0-9]\/[0-9]\/'
    res = re.findall(pattern, url)
    if len(res) == 1:
        n = res[0][5:-1].split('/')
        ssn = 'S'
        if n[0] in ['W', 'I']:
            ssn = 'W'
        return [ssn, n[1], n[2]]
