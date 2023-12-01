import cv2
import numpy as np


def get_limits(color):
    """
    get_limits takes a color in BGR values and return upper and lower hue values.
    example: lowerHue, upperHue = get_limits([220, 140, 255])
    """

    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    #Get the hue value
    hue = hsvC[0][0][0]
    spread=10
    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - spread, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + spread, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - spread, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + spread, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit


def find_pink_imported_img(img):
    """
    find_pink takes the path to image as input and return True if pink was detected
    example: find_pink("raw_data/flowers/rose/9185768268_1e48d4d119_c.jpg")
    """
    #set default return value
    pink_value = 0

    #Define pink in BGR color space
    #pink = [220, 140, 255]
    pink = [149, 97, 255]

    #Get limits of pink
    lowerHue, upperHue = get_limits(pink)

    #Load the image
    #img = cv2.imread(image_path)
    #Convert image from BGR into HSV color space
    hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Define mask
    mask = cv2.inRange(hsvImage, lowerHue, upperHue)

    #Identify how much pink is in the image
    unique, counts = np.unique(mask, return_counts=True)

    #threshold for amount of pink needed in the image
    pink_threshold = 0.005

    #check if pink was detected
    if counts.shape[0] == 2:
        #enough pink
        if counts[1] / counts[0] > pink_threshold:
            pink_value = 2
        else:
            #some pink
            pink_value = 1

    return pink_value
