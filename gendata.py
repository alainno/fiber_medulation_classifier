import cv2 as cv
import os
from pathlib import Path
import json

def cropImage(img, bbox):
    x1,y1 = bbox[0],bbox[1]
    x2 = x1 + bbox[2]
    y2 = y1 + bbox[3]
    return img[y1:y2,x1:x2]


def generateImages(source_dir, target_dir):
    #print(source_dir)
    
    json_file = open(os.path.join(source_dir, '_annotations.coco.json'))
    data = json.load(json_file)
    json_file.close()
    
    categorias = [category['name'] for category in data['categories']]
    images = [image['file_name'] for image in data['images']]
    
    for annotation in data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        print(f'save crop from image: {images[image_id]} at folder: {categorias[category_id]}')

        #img = cv.imread(f'train/{images[image_id]}')
        img = cv.imread(os.path.join(source_dir, images[image_id]))
        #img = img[:,:,::-1]

        cropped = cropImage(img, annotation['bbox'])

        #dir_path = f'data/train/{categorias[category_id]}'
        dir_path = os.path.join(target_dir, categorias[category_id])

        Path(dir_path).mkdir(parents=True, exist_ok=True)

        filename = str(annotation['id']).zfill(4) + '.jpg'

        #cv.imwrite(dir_path + '/' + filename, cropped[:,:,::-1])
        cv.imwrite(os.path.join(dir_path, filename), cropped)


if __name__ == "__main__":
    
    #print('hello world')

    generateImages(source_dir = 'train', target_dir = 'data')
