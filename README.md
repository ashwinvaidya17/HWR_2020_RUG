# HWR_2020_RUG

## Group 5 (DEV-NN)

Code for Handwriting Recognition Course 2020 RUG

---

Authors:

- Hari Vidharth - s4031180
- Krishnakumar Santhakumar - s4035992
- Dhawal Salvi - s4107624
- Ashwin Vaidya - s3911888

## General Overview

---

The full code piplines is in the main.py code.
The **lines** generated folder contains the segmented lines. The **segmented_characters** generated folder contains contains the characters which are segmented from the lines.

## Pre-requisites
---
Make sure that the pip has been upgraded so that latest version on tensorflow is installed. Also ensure that your are using Python 3.
`pip3 install --upgrade pip`

Then install the requirements
`pip3 install -r requirements.txt`

## Commands

---

To run the code follow the command and enter the folder which contains the images of the documents. Make sure to install the dependencies mentioned in requirements.txt

`python3 main.py --image path/to/image_folder`

### Example

`python3 main.py --image ./test_images`

## Modules

---

**line_segmentator** module contains two scripts. They are used to segment the given document into lines. `utils.py` contains code which aids is finding rotation on the document, calculating projection profile and A\*.

**character_segmentor** contains two scripts. The `ConnectedComponents.py` does a rough segmentation on an image of a line into characters and words. The `template_matching.py` script does template matching on the rough segmentation to get a more fine grained segmentation.

**character_recognition** module contains script to recognize the segmented characters.

**style_classification** module contains styleClassificationTest script to perform the final period classification using the segmented characters.
