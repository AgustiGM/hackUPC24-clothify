import data_formatter
import Annoy
import cv2


def print_and_show(result, distances, values):
    my_print(result, distances, values)
    cv2.imshow('Query Image', cv2.resize(cv2.imread(queryImagePath), (500, 500)))
    for (i, r) in enumerate(result):
        cv2.imshow('Result Image ' + str(i), cv2.resize(cv2.imread(f'res/images/{values[result[i]]}'), (500, 500)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def my_print(result, distances, values):
    print(result)
    print(distances)
    for (i, r) in enumerate(result):
        print(values[r])


queryImagePath = 'res/images/59/image1.jpg'
image = cv2.imread(queryImagePath)

# (result, distances, values) = Annoy.get_images(csvdata='res/images.csv', k_search=5, image = image)
# print_and_show(result, distances, values)

# distances_means = []
# for i in range(10):
#     (result, distances, values) = Annoy.get_images(csvdata='res/images.csv', k_search=i+1, image = image)
#     distances_means.append(sum(distances) / len(distances))
#
# for(i, d) in enumerate(distances_means):
#     print(f'{i+1} -> {d}')
# biggest_distance = max(distances_means)
# biggest_distance_index = distances_means.index(biggest_distance)
# Annoy.get_images_by_index(image, index_values=(0,1,2), n_neighbours=5)

(result, distances, values) = Annoy.get_images(csvdata='res/images.csv',n_neighbours= 10, image = image)
print_and_show(result, distances, values)