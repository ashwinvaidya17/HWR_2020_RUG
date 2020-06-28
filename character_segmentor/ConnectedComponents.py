import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from skimage.filters import threshold_sauvola
from skimage.morphology import skeletonize, thin
import tqdm


def segment_lines(docs_path, image_name, output_path, lines):
    save_loc = output_path + '/' + lines + \
        "/{:04d}/".format(int(image_name.split('.')[0]))
    os.makedirs(save_loc, exist_ok=True)
    original_image = cv2.imread(os.path.join(
        docs_path, lines, image_name), cv2.IMREAD_GRAYSCALE)
    line_image = original_image.copy()  # cv2.blur(original_image, (15, 15))
    boxes_locations = []

    # plt.show()
    window_size = 25
    thresh_sauvola = threshold_sauvola(line_image, window_size=window_size)
    binary_sauvola = line_image > thresh_sauvola
    binary_sauvola = np.uint8(binary_sauvola)
    ctrs, hier = cv2.findContours(
        binary_sauvola.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(tqdm.tqdm(sorted_ctrs)):
        x, y, w, h = cv2.boundingRect(ctr)

        roi = line_image[y:y + h, x:x + w]
        # plt.imshow(roi, 'gray')
        # plt.show()
        area = w*h
        if area > 900 and area < 100000:
            boxes_locations.append([x, y, x + w, y + h])

    for i, box in tqdm.tqdm(enumerate(boxes_locations)):
        x1, y1, x2, y2 = box
        character_img = original_image[y1:y2, x1:x2].copy()
        plt.imsave(save_loc + '/' +
                   "{:04d}".format(i)+'.jpg', character_img, cmap='gray')


def iterate_over_folders(docs_path, output_images_path):
    for lines in os.listdir(docs_path):
        for image_name in tqdm.tqdm(os.listdir(os.path.join(docs_path, lines))):
            segment_lines(docs_path, image_name, output_images_path, lines)


if __name__ == "__main__":
    docs_path = "C:/Users/ashwi/Desktop/Handwriting Recognition/Codes/output_images/line_images"
    output_images_path = 'C:/Users/ashwi/Desktop/Handwriting Recognition/Codes/output_images/character_images'
    iterate_over_folders(docs_path, output_images_path)
