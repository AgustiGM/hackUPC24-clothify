import cv2
import os
import glob

def format_images(folder_path = 'res/images'):
    data, labels, index = [], [], []

    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    for folder in folders:
        folder_name = folder
        images = glob.glob(os.path.join(folder_path, folder, '*.jpg'))[:3]  # Adjust extension as per your requirement

        for image_path in images:
            index.append(folder_name+"/"+os.path.basename(image_path))
            image = cv2.imread(image_path)
            image = cv2.resize(image, (32,32))
            labels.append(folder_name)
            data.append(image.flatten())

    return data, labels, index

def format_images_and_save(folder_path = 'res/images', save_path = 'res/images.csv'):
    data, labels, index = format_images(folder_path)
    with open(save_path, 'w') as file:
        for i in range(len(data)):
            file.write(f'{index[i]};{",".join(str(x) for x in data[i])};{labels[i]}\n')
    return data, labels, index

def load_images_from_csv(file_path = 'res/images.csv'):
    data, labels, index = [], [], []
    if(not os.path.exists(file_path)):
        return format_images_and_save(folder_path='res/images', save_path=file_path)
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split(';')
            index.append(parts[0])
            data.append([int(x) for x in parts[1].split(',')])
            labels.append(parts[2])
    return data, labels, index


# (a,b,c) = format_images_and_save('res/images', 'res/images.csv')
