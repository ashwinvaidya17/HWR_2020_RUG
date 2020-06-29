import numpy as np
import os
import cv2
import tensorflow as tf


def save_document(chars, output_file):
    # print(chars)
    f = open(f"output\\{output_file}.txt", "a+", encoding='utf-8')
    if len(chars) != 0:
        f.writelines(chars)
        f.writelines(f"\n")
    f.close()


def pre_process_image(img):
    img = cv2.resize(img, (32, 49))
    img = img.reshape(1, 49, 32, 1)
    img = img / 255.0
    return img


def delete_previous_output():
    read_file = "output"
    if not os.path.exists(read_file):
        os.mkdir(read_file)

    filelist = os.listdir(read_file)
    if len(filelist) != 0:
        for files in filelist:
            os.remove(os.path.join(read_file, files))


def charRecog_main(test_file):
    char_class = (
        "\u05D0", "\u05E2", "\u05D1", "\u05D3", "\u05D2", "\u05D4", "\u05D7", "\u05DB", "\u05DA", "\u05DC", "\u05DE",
        "\uFB3E", "\u05DF", "\uFB40", "\u05E4", "\u05E3", "\u05E7", "\u05E8", "\u05E1", "\u05E9", "\u05EA", "\u05D8",
        "\u05E5", "\uFB46", "\u05D5", "\u05D9", "\u05D6")
    model = tf.keras.models.load_model(f"models\\HR_char_recognition.h5")
    # model.summary()
    #output_files = os.listdir("segmented_characters")
    output_file = test_file
    #delete_previous_output()
    #for output_file in output_files:
    rootdir = f"segmented_characters\\{output_file}"
    for subdir, dirs, files in os.walk(rootdir):
        char_predict = []
        i = 0
        for filename in files:
            img_test = cv2.imread(f"{subdir}\\{filename}", 0)
            img_height, img_width = img_test.shape[0], img_test.shape[1]
            img_test = pre_process_image(img_test)
            if (img_height / img_width) > 0.23:
                y = model.predict(img_test, batch_size=None)
                confidence = np.max(y) * 100
                # print(f"{i} predicted: {test_class[np.argmax(y)]} ({char_class[np.argmax(y)]}) with {confidence}% ---- {filename}")
                if confidence > 25:
                    char_predict.append(char_class[np.argmax(y)])
                i = i + 1
        char_predict.reverse()
        save_document(char_predict, output_file)
        # print(f"--------------------------------------------------------------------------------------")
        print(f"Created {output_file}.txt containing Hebrew Characters")


#if __name__ == "__main__":
    #charRecog_main(test_file)
