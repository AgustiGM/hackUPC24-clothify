import annoy as an
from joblib.numpy_pickle_utils import xrange
import cv2

def prepare_flattened_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (32,32))
    return image.flatten()
def load_images_from_csv(file_path='res/images.csv'):
    data, labels, index = [], [], []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split(';')
            index.append(parts[0])
            data.append([int(x) for x in parts[1].split(',')])
            labels.append(parts[2])
    return data, labels, index

(data, labels, values) = load_images_from_csv()


size_of_item = len(data[0])
number_of_items = len(data)
number_of_sets = len(set(labels))

index_tree = an.AnnoyIndex(size_of_item, 'angular')
for i in range(number_of_items):
    index_tree.add_item(i, data[i])

index_tree.build(number_of_sets) # 50 trees
index_tree.save('test.tree')

# …

u = an.AnnoyIndex(size_of_item, 'angular')
u.load('test.tree') # super fast, will just mmap the file

queryImagePath = 'res/images/11/image0.jpg'

image = prepare_flattened_image(queryImagePath)
result = u.get_nns_by_vector(image, 10);

print(result)
for(i, r) in enumerate(result):
    print(values[r])
cv2.imshow('Query Image', cv2.resize(cv2.imread(queryImagePath), (500,500) ))
for(i, r) in enumerate(result):
    cv2.imshow('Result Image '+str(i), cv2.resize(cv2.imread(f'res/images/{values[result[i]]}'), (500,500)))
# Wait indefinitely until a key is pressed
cv2.waitKey(0)

    # Close all OpenCV windows
cv2.destroyAllWindows()