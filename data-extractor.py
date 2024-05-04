import requests
import os
import shutil
import csv


def create_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


root_directory = 'images'
with open('inditextech_hackupc_challenge_images.csv') as file:
    data = csv.reader(file)
    for idx, element in enumerate(data):
        if 0 < idx < 251:
            directory = f'{root_directory}{os.sep}{str(idx)}'
            create_directory(directory)
            for i, url in enumerate(element):
                if len(url) > 0:
                    image = requests.get(url)
                    if image.status_code == 200:
                        with open(f'.{os.sep}{directory}{os.sep}image{i}.jpg', 'wb') as f:
                            f.write(image.content)
                    else:
                        shutil.rmtree(directory)
                        break
        if idx % 10 == 0:
            print(f'Iteration:{idx}')
