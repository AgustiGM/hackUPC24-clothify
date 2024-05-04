import annoy as an
from joblib.numpy_pickle_utils import xrange
import cv2
import os
import glob

data = []
values = []
labels = []
def capture_images():
    folder_path = 'res/images'
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    for folder in folders:
        folder_name = folder
        images = glob.glob(os.path.join(folder_path, folder, '*.jpg'))[:3]  # Adjust extension as per your requirement

        # print("Folder:", folder_name)
        for image_path in images:
            values.append(folder_name+"/"+os.path.basename(image_path))
            image = cv2.imread(image_path)
            image = cv2.resize(image, (32,32))
            labels.append(folder_name)
            data.append(image.flatten())


capture_images()


f = 3072    #len(data)
t = an.AnnoyIndex(f)
for i in xrange(len(data)):
    t.add_item(i, data[i])

t.build(len(set(labels))) # 50 trees
t.save('test.tree')

# …

u = an.AnnoyIndex(f)
u.load('test.tree') # super fast, will just mmap the file
# print (u.get_nns_by_item(0, 3)) # will find the 1000 nearest neighbors
queryImagePath = 'res/images/11/image0.jpg'

image = cv2.imread(queryImagePath)
image = cv2.resize(image, (32,32)).flatten()
result = u.get_nns_by_vector(image, 5);
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