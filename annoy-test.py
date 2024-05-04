import os

import annoy as an
import cv2
import pandas as pd
from utils import get_hog_feature_vector
from object_detector import extract_important_object

df = pd.read_pickle('dataframe_images.csv')

vals = df['features'].to_numpy()
f = 3072  #len(data)
t = an.AnnoyIndex(f, metric='angular')
for i, data_point in enumerate(vals):
    t.add_item(i, data_point)

t.build(len(set(df['labels'])))  # 50 trees
t.save('test.tree')

u = an.AnnoyIndex(f, metric='angular')
u.load('test.tree')  # superfast, will just mmap the file
# print (u.get_nns_by_item(0, 3)) # will find the 1000 nearest neighbors
queryImagePath = f'processed_images{os.sep}89{os.sep}image0.jpg'

image = cv2.imread(queryImagePath)
# cropped_image = extract_important_object(image)
processed_image = cv2.resize(image, (32, 32)).flatten()
(result, distances) = u.get_nns_by_vector(processed_image, 5, search_k=5, include_distances=True)

print(result)
routes = df['routes'].to_list()
for (i, r) in enumerate(result):
    print(routes[r])
    print(distances[i])
cv2.imshow('Query Image', image)
for (i, r) in enumerate(result):
    s = os.sep
    rt = s.join([str(routes[r][0]), routes[r][1]])
    rt = f'images{os.sep}{rt}'
    im = cv2.imread(rt)
    cv2.imshow(f'Result Image {i}', cv2.resize(im, (500, 750)))
# Wait indefinitely until a key is pressed
cv2.waitKey(0)

cv2.destroyAllWindows()
