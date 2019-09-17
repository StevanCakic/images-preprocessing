import cv2
import sys
import os

def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (real_height, real_width) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        ratio = height / float(real_height)
        dim = (int(real_width * ratio), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        ratio = width / float(real_width)
        dim = (width, int(real_height * ratio))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def main(images):
    root_folder = ".\\images" # root for write folder
    for filename in os.listdir(images):

        output_location = root_folder + "\\preprocessed\\" + filename

        # read image
        img = cv2.imread(f'{images}\\{filename}')
        # cv.imshow("Original image", img)

        # resized image
        resized_img = image_resize(img, 500, 100)
        # cv2.imshow("Original resized image", resized_img)

        # Convert image to gray
        img_gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray image", img_gray)

        # Get resized image dimensions
        rows, _ = img_gray.shape

        # Get horizontal size (for creating kernel to remove horizontal lines)
        horizontalsize = int(rows / 35)

        # Creating kernel for dilate
        # MOTPH_ELLIPSE works best
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, horizontalsize))

        # Create dilate image
        # Docs: https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
        dilated_image = cv2.dilate(img_gray, kernel)
        # cv2.imshow("Dilate", dilated_image)
        
        # Blured by Gaussian blur
        blured_image = cv2.GaussianBlur(dilated_image, (3, 5), 0)
        # cv2.imshow("Blured by Gaussian blur", blured_image)

        # Otsu thresholding
        _, th_otsu_image = cv2.threshold(blured_image, 0, 255, cv2.THRESH_OTSU)
        # cv2.imshow("Otsu", th_otsu_image)
        
        # Erode image, to get bolder numbers
        result_image = cv2.erode(th_otsu_image, kernel)

        # cv2.imshow("Result", result_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imwrite(output_location, result_image)

if __name__ == "__main__":
    IMAGES_FOLDER = sys.argv[1] # images read folder
    main(IMAGES_FOLDER)
