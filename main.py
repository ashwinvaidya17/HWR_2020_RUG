from line_segmenter import line_segment
import os
import shutil
import argparse
from character_segmentor import ConnectedComponents, template_matching
from character_recognition import recognise_hebrew_chars

if __name__ == "__main__":
    # ----------------------------- line segmentation -----------------------------------------------
    arg = argparse.ArgumentParser()
    arg.add_argument('--image', metavar='I', type=str,
                     help="enter the image path")
    img_parase = arg.parse_args()
    img_path = img_parase.image
    print(f"------------------------------>> Line segmentation <<------------------------------------")
    curr_dir = os.getcwd()
    if not "lines" in os.listdir():
        os.mkdir("lines")
    for img in os.listdir(img_path):
        split1 = img.split('.')
        line_segment.run(img_path+"/"+img, "lines/"+split1[0], curr_dir)

        os.chdir(curr_dir)
        print(f"# Line segmentation completed for image :{str(img)}#")

        # -------------------------- character segmentation -------------------------------------------
        print(f"------------------------------>> character segmentation <<------------------------------------")
        ConnectedComponents.iterate_over_folders(os.path.join(
            os.getcwd(), 'lines'), os.path.join(os.getcwd(), 'segmented_characters'))
        template_matching.iterate_over_characters(os.path.join(
            os.getcwd(), 'segmented_characters/'), os.path.join(os.getcwd(), 'character_images/Images/'))
        print(f"# Completed Character Segmentation for image :{str(img)}")

    # -------------------------- character Recognition -------------------------------------------
    recognise_hebrew_chars.charRecog_main()
