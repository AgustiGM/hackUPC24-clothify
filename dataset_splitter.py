import csv
import os

import pandas as pd
from utils import get_attributes_from_url

route = 'inditextech_hackupc_challenge_images.csv'

data = {}

with open(route, 'r') as file:
    reader = csv.reader(file)
    next(reader, None)
    for index, line in enumerate(reader):
        attributes = get_attributes_from_url(line[0])
        if attributes is not None:
            id_key = '_'.join(attributes)
            if id_key not in data.keys():
                data[id_key] = {}
            data[id_key][index] = line

for category in data.keys():
    ids = data[category].keys()
    urls = data[category].values()
    a = zip(ids, urls)
    data_points = []
    for product_id, product_urls in a:
        data_point = [product_id] + product_urls
        data_points.append(data_point)
    df = pd.DataFrame(data_points, columns=['id', 'url1', 'url2', 'url3'])

    df.to_csv(f'csv{os.sep}{category}.csv')
