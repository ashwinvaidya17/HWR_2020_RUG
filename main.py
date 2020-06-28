from line_segmenter import line_segment
import os
import shutil
import argparse




if __name__=="__main__":
    # ----------------------------- line segmentation -----------------------------------------------
    arg=argparse.ArgumentParser()
    arg.add_argument('--image',metavar='I',type=str,help="enter the image path")
    img_parase=arg.parse_args()
    img=img_parase.image
    print(f"------------------------------>> Line segmentation <<------------------------------------")
    curr_dir=os.getcwd()
    if not "lines" in os.listdir():
        os.mkdir("lines")
    split1=img.split('.')
    split2=split1[0].split('/')
    line_segment.run(img,"lines/"+split2[-1],curr_dir)

    print("# Line segmentation completed #")

    # -------------------------- character segmentation -------------------------------------------
    print(f"------------------------------>> character segmentation <<------------------------------------")
