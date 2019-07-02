import sys
import os
from PIL import Image
import pytesseract

# This path stores location to to executable tesseract (maybe different on your machine)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

# https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc
# Simple image to string

# setovati folder gdje se nalaze slike za recognize
IMAGES_FOLDER = sys.argv[1]
# proci kroz folder sa slikama i uporediti da li se broj slaze sa nazivom slike do _
text = ""
for filename in os.listdir(IMAGES_FOLDER):
    index_of_ = filename.find('_')
    index_of_dot = filename.find(".")
    new_filename = ""
    version = 1
    if index_of_ > -1:
        new_filename = filename[0:index_of_]
        version = filename[index_of_ + 1: index_of_dot]
    else:
        new_filename = filename[0:index_of_dot]
    image_path = f'{IMAGES_FOLDER}\{filename}'
    print("Processing: " + image_path)
    SERIAL_NUMBER = pytesseract.image_to_string(Image.open(image_path), config='--psm 13')
    DIGITS = list(filter(lambda str: str.isdigit(), SERIAL_NUMBER))
    RESULT = "".join(DIGITS)
    text += "Version:" + str(version) + ";Original:" + new_filename + ";Recognized:" + RESULT + "\n"

with open("output_tesseract.txt", "w", encoding="utf-8") as f:
    f.write(text)