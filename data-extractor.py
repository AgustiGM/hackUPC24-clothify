import requests
import os
import shutil
import csv

with open('inditextech_hackupc_challenge_images.csv') as file:
    data = csv.reader(file)
    for idx, element in enumerate(data):
        if 0 < idx < 2:
            directory = f'{str(idx)}'
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)
            for i, url in enumerate(element):
                image = requests.get(url)
                with open(f'.{os.sep}{directory}{os.sep}image{i}.jpg', 'wb') as f:
                    f.write(image.content)


