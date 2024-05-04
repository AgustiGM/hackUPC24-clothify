import os

import annoy as an
import cv2
import pandas as pd
from utils import get_hog_feature_vector

df = pd.read_pickle('dataframe.csv')

vals = df['features'].to_numpy()
f = 1764    #len(data)
t = an.AnnoyIndex(f, metric='angular')
for i, data_point in enumerate(vals):
    t.add_item(i, data_point)

t.build(len(set(df['labels']))) # 50 trees
t.save('test.tree')

# …

u = an.AnnoyIndex(f)
u.load('test.tree') # super fast, will just mmap the file
# print (u.get_nns_by_item(0, 3)) # will find the 1000 nearest neighbors
queryImagePath = f'images{os.sep}23{os.sep}image0.jpg'

image = cv2.imread(queryImagePath)

result = u.get_nns_by_vector(get_hog_feature_vector(image), 5)

print(result)
routes = df['routes'].to_list()
for(i, r) in enumerate(result):
    print(routes[r])
cv2.imshow('Query Image', cv2.resize(cv2.imread(queryImagePath), (500,500) ))
for(i, r) in enumerate(result):
    s = os.sep
    rt = s.join([str(routes[r][0]),routes[r][1]])
    rt = f'images{os.sep}{rt}'
    im = cv2.imread(rt)
    cv2.imshow(f'Result Image {i}', cv2.resize(im, (500,500)))
# Wait indefinitely until a key is pressed
cv2.waitKey(0)

    # Close all OpenCV windows
cv2.destroyAllWindows()