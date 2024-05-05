import csv
import os

import annoy as an
from joblib.numpy_pickle_utils import xrange
import cv2
from data_formatter import *
from object_detector import extract_important_object


def prepare_flattened_image(image):
    image = extract_important_object(image)
    image = cv2.resize(image, (32,32))
    return image.flatten()


def get_images(csvdata, image, n_neighbours = 5):
    if(not os.path.exists(csvdata)):
        (data, labels, values) = format_images_and_save(folder_path='res/images', save_path='res/images.csv')
    else:
        (data, labels, values) = load_images_from_csv(csvdata)

    size_of_item = len(data[0])
    number_of_items = len(data)
    number_of_sets = 50

    index_tree = an.AnnoyIndex(size_of_item, 'angular')
    for i in range(number_of_items):
        index_tree.add_item(i, data[i])

    index_tree.build(number_of_sets)
    index_tree.save('test.tree')


    u = an.AnnoyIndex(size_of_item, 'angular')
    u.load('test.tree')


    image = prepare_flattened_image(image)
    (result, distances) = u.get_nns_by_vector(image, n_neighbours, search_k=5, include_distances=True)


    return result, distances, values


def get_index(index_values, size_of_item):
    index = an.AnnoyIndex(size_of_item, 'angular')
    index.load(f'res{os.sep}images{os.sep}{"-".join(index_values)}.tree')
    return index


def get_values(index_values):
    with open(f'res{os.sep}images{os.sep}{"-".join(index_values)}.csv', 'r') as file:
        values = []
        reader = csv.reader(file)
        for row in reader:
            values = row
    return values


def get_images_by_index(image, index_values = (0,0,0), n_neighbours = 5):
    values = get_values(index_values)

    image = prepare_flattened_image(image)
    index_tree = get_index(index_values, len(image))

    (result, distances) = index_tree.get_nns_by_vector(image, n_neighbours, search_k=5, include_distances=True)

    return result, distances, values

