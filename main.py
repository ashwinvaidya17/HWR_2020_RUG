from line_segmenter import line_segment
import os
import shutil
import argparse


if __name__=="__main__":
    # ----------------------------- line segmentation -----------------------------------------------
    arg=argparse.ArgumentParser()
    arg.add_argument('--image',metavar='I',type=str,help="enter the image path")
    img_parase=arg.parse_args()
    img_path=img_parase.image
    print(f"------------------------------>> Line segmentation <<------------------------------------")
    curr_dir=os.getcwd()
    if not "lines" in os.listdir():
        os.mkdir("lines")
    for img in os.listdir(img_path):
        split1=img.split('.')
        line_segment.run(img_path+"/"+img,"lines/"+split1[0],curr_dir)

    print("# Line segmentation completed #")

    # -------------------------- character segmentation -------------------------------------------
    print(f"------------------------------>> character segmentation <<------------------------------------")

