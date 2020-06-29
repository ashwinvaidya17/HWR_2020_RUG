import cv2
import os
import statistics


def max_dim(read_path):
    height = []
    width = []
    j = 0
    for filename in os.listdir(read_path):
        if filename.endswith(".jpg"):
            img = cv2.imread(f"{read_path}/{filename}", -1)
            height.append(int(img.shape[0]))
            width.append(int(img.shape[1]))

    j = height.index(max(height))

    return width[j], height[j]


def avg_dim(read_path):
    height = []
    width = []
    j = 0
    for filename in os.listdir(read_path):
        if filename.endswith(".jpg"):
            img = cv2.imread(f"{read_path}/{filename}", -1)
            height.append(int(img.shape[0]))
            width.append(int(img.shape[1]))
    w = int(statistics.median(width))
    h = int(statistics.median(height))
    return w, h


def save_image_new_dim(r_folder, s_folder, l_name):
    for l in l_name:
        read_path = os.path.join(r_folder, l)
        dim = avg_dim(read_path)
        os.mkdir(f"{s_folder}/{l}")
        i = 0
        for filename in os.listdir(read_path):
            if filename.endswith(".jpg"):
                i = i + 1
                img = cv2.imread(f"{read_path}/{filename}", -1)
                if i == 1:
                    print(img.shape)
                img = cv2.resize(img, dim)
                save_path = os.path.join(s_folder, l)
                cv2.imwrite(f"{save_path}/{l}_{i}.jpg", img)


def main():
    read_path = "character_images"
    read_folder = read_path + "Images"
    save_path = "character_images"
    save_folder = save_path + "Images_first_preprocess"

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    label_name = (
        "Alef", "Ayin", "Bet", "Dalet", "Gimel", "He", "Het", "Kaf", "Kaf-final", "Lamed", "Mem", "Mem-medial",
        "Nun-final", "Nun-medial", "Pe", "Pe-final", "Qof", "Resh", "Samekh", "Shin", "Taw", "Tet", "Tsadi-final",
        "Tsadi-medial", "Waw", "Yod", "Zayin")

    save_image_new_dim(read_folder, save_folder, label_name)


if __name__ == "__main__":
    main()
