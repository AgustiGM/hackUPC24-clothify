import csv
import pandas as pd
import re


def find_attributes(url):
    pattern = r'[0-9]{4}\/[A-Z]\/[0-9]\/[0-9]\/'
    res = re.findall(pattern, url)
    if len(res) == 1:
        return res[0][5:-1]
    return None


route = 'inditextech_hackupc_challenge_images.csv'

data = {}
seasons = set()
product_type = set()
section = set()

with open(route, 'r') as file:
    reader = csv.reader(file)
    next(reader, None)
    for index, line in enumerate(reader):
        category = find_attributes(line[0])
        if category is not None:
            n = category.split('/')
            ssn = 'S'
            if n[0] in ['W', 'I']:
                ssn = 'W'
            seasons.add(ssn)
            product_type.add(n[1])
            section.add(n[2])
            id_key = '_'.join([ssn, n[1], n[2]])
            if id_key not in data.keys():
                data[id_key] = {}
            data[id_key][index] = line


for category in data.keys():
    ids = data[category].keys()
    urls = data[category].values()
    a = zip(ids,urls)
    data_points = []
    for product_id, product_urls in a:
        data_point = [product_id] + product_urls
        data_points.append(data_point)
    df = pd.DataFrame(data_points, columns=['id','url1','url2','url3'])
    df.to_csv(f'{category}.csv')


