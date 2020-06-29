from line_segmenter import line_segment
import os
import shutil
import argparse
from character_segmentor import ConnectedComponents, template_matching
from character_recognition import recognise_hebrew_chars
from style_classification.styleClassificationTest import styleClassification

if __name__ == "__main__":
    recognise_hebrew_chars.delete_previous_output()
    # ----------------------------- line segmentation -----------------------------------------------
    arg = argparse.ArgumentParser()
    arg.add_argument('--image', metavar='I', type=str,
                     help="enter the image path", required=True)
    img_parase = arg.parse_args()
    img_path = img_parase.image
    print(f"------------------------------>> Line segmentation <<------------------------------------")
    curr_dir = os.getcwd()
    if not "lines" in os.listdir():
        os.mkdir("lines")
    if "lines" in os.listdir():
        shutil.rmtree("lines")
        os.mkdir("lines")
        
    for img in os.listdir(img_path):
        split1 = img.split('.')
        line_segment.run(img_path+"/"+img, "lines/"+split1[0], curr_dir)
        print(f"# Line segmentation completed for image :{str(img)}#")
        os.chdir(curr_dir)
        
        print(f"------------------------------>> character segmentation <<------------------------------------")
        ConnectedComponents.iterate_over_folders(os.path.join(
            os.getcwd(), 'lines', split1[0]), os.path.join(os.getcwd(), 'segmented_characters'), split1[0])
        template_matching.iterate_over_characters(os.path.join(
            os.getcwd(), 'segmented_characters', split1[0]), os.path.join(os.getcwd(), 'character_images/Images/'))
        print("# Completed Character Segmentation")

        # -------------------------- character Recognition -------------------------------------------
        print(f"------------------------------>> character recognition <<------------------------------------")
        recognise_hebrew_chars.charRecog_main(split1[0])
        print("# Completed Character Recognition")

        print(f"------------------------------>> style classification <<------------------------------------")
        styleClassification(path_to_char_recog_model="./models/HR_char_recognition.h5", path_to_segmented_images="./segmented_characters", document_name=split1[0])
        print("# Completed Style Classification")
