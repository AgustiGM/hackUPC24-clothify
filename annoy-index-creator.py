import csv

import pandas as pd
import numpy as np
import os
import cv2
import glob
import annoy as an
import re
import requests

from utils import create_directory
from data_formatter import *


def download_data():
    csvsroutes = 'res/csvs/'
    files = os.listdir(csvsroutes)

    # Iterate over each file in the folder
    for file_name in files:
        # Check if the file is a CSV
        if file_name.endswith('.csv'):
            file_path = os.path.join(csvsroutes, file_name)

            # EXTRACT INDEX VALUES
            index_values = file_path.split('_')
            season = (index_values[0].split('/'))[-1]
            product_type = int(index_values[1])
            section = int(index_values[2].split('.')[0])

            if season == 'W':
                # Load the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                if 'Unnamed: 0' in df.columns:
                    df.drop('Unnamed: 0', axis=1, inplace=True)

                print("...downloading images for ", file_path)
                for index, row in df.iterrows():
                    if index < 100:
                        create_directory('res/images/'+str(row['id']))
                        for i in range(1, 4):
                            # if i == 2:
                            # print(row['url'+str(i)])
                            # print("---"+row['url'+str(i)].__class__.__name__)
                            if row['url'+str(i)].__class__.__name__ != 'str':
                                print("...skipping image ", index)
                            else:
                                url = row['url'+str(i)]
                                image = requests.get(url)
                                if image.status_code == 200:
                                    with open(f'''.{os.sep}res{os.sep}images{os.sep}{row['id']}{os.sep}image{i}.jpg''', 'wb') as f:
                                        f.write(image.content)

                create_index((season,product_type,section), df)

def create_index(index_values, dataframe):
    print("...creating index for ", index_values)
    data, labels, values = [], [], []

    season = index_values[0]
    product_type = index_values[1]
    section = index_values[2]


    number_of_images = 100 if dataframe.shape[0] > 100 else dataframe.shape[0]
    #TODO: maybe is number_of_images + 1? check this
    for i in range(number_of_images):

        # Load all images in folder
        folder_name = f'''res{os.sep}images{os.sep}{str(dataframe['id'][i])}{os.sep}'''
        images = glob.glob(os.path.join(folder_name, '*.jpg'))[:3]  # Adjust extension as per your requirement

        for image_path in images:
            values.append(f'{folder_name}{os.path.basename(image_path)}')
            labels.append(folder_name.split(os.sep)[-2])
            data.append(format_image(cv2.imread(image_path)))


    size_of_item = len(data[0])
    number_of_items = len(data)
    number_of_sets = len(set(labels))

    index_tree = an.AnnoyIndex(size_of_item, 'angular')
    for i in range(number_of_items):
        index_tree.add_item(i, data[i])

    index_tree.build(number_of_sets)
    index_tree.save(f'res{os.sep}images{os.sep}{season}-{product_type}-{section}.tree')

    values_filename = f'res{os.sep}images{os.sep}{season}-{product_type}-{section}.csv'
    with open(values_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(values)

    return data, labels, values

download_data()