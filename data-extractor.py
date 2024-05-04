import requests
import os
import csv

with open('inditextech_hackupc_challenge_images.csv') as file:
    data = csv.reader(file)
    for idx, element in enumerate(data):
        if 0 < idx < 2:
            os.mkdir(idx)
            for i, url in enumerate(element):
                image = requests.get(url)
                with open(i+'fle.jpg', 'wb') as f:
                    f.write(image.content)


