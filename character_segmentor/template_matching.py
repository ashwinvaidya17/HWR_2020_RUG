
import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
import tqdm
import os
import operator
import random
import argparse

output_save_path = ''
input_path = ''
character_image_path = ""
categories = []

unique_counter = 1

method = eval('cv2.TM_CCOEFF_NORMED')

orig_x = None
orig_y = None


def get_match_scores(search_image, threshold=0.52):
    match_scores = {}
    for label in categories:
        match_scores[label] = []
    for label in tqdm.tqdm(categories):
        # Take first n images
        for path in glob.glob(character_image_path+label+'/*.pgm'):
            template = cv2.imread(path, 0)
            template_x, template_y = template.shape
            scale_ratio = orig_x/template_x
            if scale_ratio > 2:  # Experiments found this scale better
                scale_ratio = 2
            search_image_x, search_image_y = search_image.shape
            # for scale in np.arange(0.2, scale_ratio, 0.1):
            y_ratio = (int)(scale_ratio*template_x)
            if y_ratio > search_image_x:
                y_ratio = search_image_x
            x_ratio = (int)(scale_ratio*template_y)
            if x_ratio > search_image_y:
                x_ratio = search_image_y
            template = cv2.resize(
                template, (x_ratio, y_ratio), interpolation=cv2.INTER_AREA)

            w, h = template.shape[::-1]
            # print(search_image.shape)
            # print(template.shape)
            try:
                res = cv2.matchTemplate(search_image, template, method)
            except Exception as e:
                print(e)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            match_scores[label].append(max_val)
    if len(match_scores) == 0:
        return
    for label in categories:
        try:
            match_scores[label] = max(match_scores[label])
        except Exception as e:
            print(e)
            print(label)
            print(match_scores)
            exit()
        if match_scores[label] < threshold:
            match_scores.pop(label, None)
    return match_scores


def split_images(input_image, top_left, h, w):
    extracted_image = input_image.copy(
    )[:top_left[1]+h, top_left[0]: top_left[0]+w]
    first_image = input_image.copy()[:top_left[1]+h, :top_left[0]]
    second_image = input_image.copy()[:top_left[1]+h, top_left[0]+w:]

    first_image_area_ratio = (
        first_image.shape[0]*first_image.shape[1])/(input_image.shape[0]*input_image.shape[1])

    extracted_image_area_ratio = (
        extracted_image.shape[0]*extracted_image.shape[1])/(input_image.shape[0]*input_image.shape[1])

    second_image_area_ratio = (
        second_image.shape[0]*second_image.shape[1])/(input_image.shape[0]*input_image.shape[1])

    return (extracted_image, extracted_image_area_ratio), (first_image, first_image_area_ratio), (second_image, second_image_area_ratio)


def recursive_splitting(img, recursion_depth, area_ratio, image_index, search_threshold=0.6):
    global unique_counter
    #   Base cases
    if recursion_depth > 5:  # Safety
        return

    if img is None:
        return

    unique_save_path = output_save_path + '/' + \
        "{:04d}".format(image_index) + '_' + \
        "{:04d}".format(unique_counter)+'.jpg'
    # print(unique_save_path)
    # print(orig_x, orig_y)
    if area_ratio > 0.7:  # Based on experiments
        # img = cv2.resize(img, (32, 49))
        plt.imsave(unique_save_path,
                   img, cmap='gray')
        unique_counter += 1
        return

    print("Getting match scores")
    match_scores = get_match_scores(img, search_threshold)
#     print(match_scores)
    print("Found %s matches" % len(match_scores))
    if len(match_scores.values()) == 0:
        return

    if len(match_scores) == 1:
        # img = cv2.resize(img, (32, 49))
        plt.imsave(unique_save_path,
                   img, cmap='gray')
        unique_counter += 1
        return

    max_label = max(match_scores.items(), key=operator.itemgetter(1))[0]

    best_match_details = {}
    temp_image = img.copy()
    # Take first n images
    for path in glob.glob(character_image_path+max_label+'/*.pgm'):
        template = cv2.imread(path, 0)
        # plt.imshow(template)
        # print(template.shape)
        # plt.show()
        # print(orig_x, orig_y)
        # plt.imshow(temp_image)
        # plt.show()
        template_x, template_y = template.shape
        scale_ratio = orig_x/template_x
        if scale_ratio > 2:  # Experiments found this scale better
            scale_ratio = 2
        template_scores = []
        search_image_x, search_image_y = temp_image.shape
        # for scale in np.arange(0.2, scale_ratio, 0.1):
        y_ratio = (int)(scale_ratio*template_x)
        if y_ratio > search_image_x:
            y_ratio = search_image_x
        x_ratio = (int)(scale_ratio*template_y)
        if x_ratio > search_image_y:
            x_ratio = search_image_y
        template = cv2.resize(
            template, (x_ratio, y_ratio), interpolation=cv2.INTER_AREA)

        w, h = template.shape[::-1]
        try:
            res = cv2.matchTemplate(temp_image, template, method)
        except Exception as e:
            print("Error occured while processing")
            print(e)
            return
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # plt.imshow(template)
        # print(template.shape)
        # plt.show()
        w, h = template.shape[::-1]
        best_match_details[max_val] = max_loc
    max_key = max(best_match_details.keys())
    top_left = best_match_details[max_key]
    (extracted_image, extracted_image_ar), (first_image, first_image_ar), (second_image,
                                                                           second_image_ar) = split_images(temp_image, top_left, h, w)

    #  Area ratio found based on experiments
    if extracted_image_ar < 0.2:
        extracted_image = None
    if first_image_ar < 0.2:
        first_image = None
    if second_image_ar < 0.2:
        second_image = None

    # Keep increasing threshold as image is broken down
    recursive_splitting(first_image, recursion_depth + 1,
                        first_image_ar, image_index, search_threshold+0.01)
    recursive_splitting(extracted_image, recursion_depth + 1,
                        extracted_image_ar, image_index, search_threshold+0.01)
    recursive_splitting(second_image, recursion_depth + 1,
                        second_image_ar, image_index, search_threshold+0.01)


def iterate_over_characters(input_path, character_images_path):
    global categories
    global unique_counter
    global orig_x
    global orig_y
    global output_save_path
    global character_image_path
    character_image_path = character_images_path
    categories = os.listdir(character_image_path)
    for docs in os.listdir(input_path):
        for line_character_folders in os.listdir(os.path.join(input_path, docs)):
            for input_image_path in tqdm.tqdm(glob.glob(os.path.join(input_path, docs,  line_character_folders)+"/*.jpg")):
                input_character_image = cv2.imread(input_image_path, 0)
                orig_x, orig_y = input_character_image.shape
                # Based on experiments. If the ratio is greater then it is assumed that the segemented image is a combination
                if (orig_y/orig_x) < 1.2:
                    continue
                unique_counter = 1
                output_save_path = os.path.join(
                    input_path, docs, line_character_folders)
                # todo change path for linux
                image_index = int(input_image_path.split('.')
                                  [0].split('\\')[-1])
                os.makedirs(output_save_path, exist_ok=True)
                recursive_splitting(input_character_image, 1, 0, image_index)
                os.remove(input_image_path)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     description='This file splits each character into sub-characters as the first character splitting might be coarse.')
    # parser.add_argument(
    #     '--input_path', help='Path of the coarse split characters')
    # parser.add_argument('--character_images',
    #                     help='Path to folder containing character images for use in template matching')
    # args = parser.parse_args()

    input_path = "C:/Users/ashwi/Desktop/Handwriting Recognition/Codes/output_images/character_images/"  # args.input_path
    # args.character_images
    character_image_path = "C:/Users/ashwi/Desktop/Handwriting Recognition/Images/"
    iterate_over_characters(input_path, character_image_path)
