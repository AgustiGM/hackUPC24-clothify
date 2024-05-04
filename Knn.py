# import the necessary packages
import numpy as np
import cv2
import os
import glob


# class SimpleDatasetLoader:
#     def __init__(self, preprocessors=None):
#         # store the image preprocessor
#         self.preprocessors = preprocessors
#
#         # if the preprocessors are None, initialize them as an
#         # empty list
#         if self.preprocessors is None:
#             self.preprocessors = []
#
#     def load(self, imagePaths, verbose=-1):
#         # initialize the list of features and labels
#         data = []
#         labels = []
#
#         # loop over the input images
#         for (i, imagePath) in enumerate(imagePaths):
#             # load the image and extract the class label assuming
#             # that our path has the following format:
#             # /path/to/dataset/{class}/{image}.jpg
#             image = cv2.imread(imagePath)
#             label = imagePath.split(os.path.sep)[-2]
#
#             # check to see if our preprocessors are not None
#             if self.preprocessors is not None:
#                 # loop over the preprocessors and apply each to
#                 # the image
#                 for p in self.preprocessors:
#                     image = p.preprocess(image)
#             # treat our processed image as a "feature vector"
#             # by updating the data list followed by the labels
#             data.append(image)
#             labels.append(label)
#
#         # show an update every `verbose` images
#         if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
#             print("[INFO] processed {}/{}".format(i + 1,
#                                                   len(imagePaths)))
#
#
#         # return a tuple of the data and labels
#         return (np.array(data), np.array(labels))

data = []
labels = []
def capture_images():
    folder_path = 'res/images'
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    for folder in folders:
        folder_name = folder
        images = glob.glob(os.path.join(folder_path, folder, '*.jpg'))[:3]  # Adjust extension as per your requirement

        # print("Folder:", folder_name)
        for image_path in images:
            image = cv2.imread(image_path)
            image = cv2.resize(image, (32,32))
            labels.append(folder_name)
            data.append(image.flatten())
            # print("  Image:", os.path.basename(image_path))


from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
# from python_imagesearch.imagesearch import
# from pyimagesearch.datasets import SimpleDatasetLoader
from imutils import paths
import argparse

# ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--dataset", required=True,
# 	help="path to input dataset")
# ap.add_argument("-k", "--neighbors", type=int, default=1,
# 	help="# of nearest neighbors for classification")
# ap.add_argument("-j", "--jobs", type=int, default=-1,
# 	help="# of jobs for k-NN distance (-1 uses all available cores)")
# args = vars(ap.parse_args())

capture_images()

# encode the labels as integers
le = LabelEncoder()
labels = le.fit_transform(labels)
# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
(trainX, testX, trainY, testY) = train_test_split(data, labels,test_size=0.25, random_state=40)

# train and evaluate a k-NN classifier on the raw pixel intensities
print("[INFO] evaluating k-NN classifier...")
model = KNeighborsClassifier(n_neighbors=2,
	n_jobs=-1)
model.fit(trainX, trainY)
print(testY)
print(model.predict(testX))
print(classification_report(testY, model.predict(testX)))
