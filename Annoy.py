import annoy as an
from joblib.numpy_pickle_utils import xrange
import cv2
from data_formatter import load_images_from_csv

def prepare_flattened_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (32,32))
    return image.flatten()

(data, labels, values) = load_images_from_csv()


size_of_item = len(data[0])
number_of_items = len(data)
number_of_sets = len(set(labels))

index_tree = an.AnnoyIndex(size_of_item, 'angular')
for i in range(number_of_items):
    index_tree.add_item(i, data[i])

index_tree.build(number_of_sets)
index_tree.save('test.tree')

u = an.AnnoyIndex(size_of_item, 'angular')
u.load('test.tree')

queryImagePath = 'res/images/23/image0.jpg'

image = prepare_flattened_image(queryImagePath)
(result, distances) = u.get_nns_by_vector(image, 5, include_distances=True);

print(result)
print(distances)
for(i, r) in enumerate(result):
    print(values[r])

cv2.imshow('Query Image', cv2.resize(cv2.imread(queryImagePath), (500,500) ))

for(i, r) in enumerate(result):
    cv2.imshow('Result Image '+str(i), cv2.resize(cv2.imread(f'res/images/{values[result[i]]}'), (500,500)))

cv2.waitKey(0)
cv2.destroyAllWindows()