import csv

import cv2
import numpy as np
import requests

from Annoy import get_images_by_index
from utils import get_attributes_from_url

from io import BytesIO

def print_and_show(result, distances, values):
    # my_print(result, distances, values)
    for (i, r) in enumerate(result):
        cv2.imshow('Result Image ' + str(i), cv2.resize(cv2.imread(f'{values[result[i]]}'), (500, 500)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def my_print(result, distances, values):
    print(result)
    print(distances)
    for (i, r) in enumerate(result):
        print(values[r])

def read_image_from_url(url):
    # Send a GET request to the URL to fetch the image content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Read the image content from the response
        return response.content
    else:
        print(response.status_code)
        print("Failed to fetch image from URL:", url)
        return None


def similar_images_from_url(url):
    image = read_image_from_url(url)

    if image is not None:
        arr = np.asarray(bytearray(image), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)

        index_values = get_attributes_from_url(url)

        (result, distances, values) = get_images_by_index( image, index_values=(index_values[0], index_values[1], index_values[2]), n_neighbours=5)

        urls = []


        with open('res/inditextech_hackupc_challenge_images.csv') as file:
            csv_reader = csv.reader(file)
            data_list = list(csv_reader)
            for i in result:
                first = values[i].split('\\')[2]
                second = (values[i].split('\\')[-1]).removeprefix('image').removesuffix('.jpg')
                urls.append(data_list[int(first)][int(second)])

        print(urls)
        print_and_show(result, distances, values)

url = 'https://static.zara.net/photos///2024/V/0/1/p/4424/156/800/2/w/2048/4424156800_1_1_1.jpg?ts=1713531158636'
url2 = 'https://static.zara.net/photos///2024/V/0/2/p/3920/423/507/2/w/2048/3920423507_6_1_1.jpg?ts=1707469389327'
url3 = 'https://static.zara.net/photos///2024/V/0/1/p/4424/156/800/2/w/2048/4424156800_1_1_1.jpg?ts=1713531158636'
url4 = 'https://static.zara.net/photos///2024/V/4/1/p/1649/052/999/2/w/2048/1649052999_6_1_1.jpg?ts=1701276936976'

similar_images_from_url(url4)
