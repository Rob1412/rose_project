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
    find_pink takes an image as input and returns "0" for no pink found,
    "1" for some pink found, and "2" for enough pink found
    example: find_pink(image)
    """
    #set default return value
    pink_value = 0

    #Define pink in BGR color space
    #pink = [220, 140, 255]
    pink = [149, 97, 255]

    #Get limits of pink
    lowerHue, upperHue = get_limits(pink)

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

def multi_color_detect_img(img):
    """
    find_pink takes an image as input and returns "0" for no pink found,
    "1" for some pink found, and "2" for enough pink found
    example: find_pink(image)
    """
    #set default return value
    pink_value = 0
    colorthresholds={}
    colors={
        'green':[42,239,60],
        'yellow':[15,255,254],
        'orange':[18,146,249],
        'red':[22,13,246],
        'lila':[239,13,246],
        'purple':[237,5,145],
        'blue':[237,9,5],
        'aquamarin':[237,127,5],
        'turquoise':[237,198,5],
        'mint':[162,237,5],
        'white':[245,245,245],
        'black':[10,10,10]
    }
    #Define pink in BGR color space
    #pink = [220, 140, 255]
    for c in colors.keys():

    #Get limits of c
        lowerHue, upperHue = get_limits(colors[c])

    #Convert image from BGR into HSV color space
        hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Define mask
        mask = cv2.inRange(hsvImage, lowerHue, upperHue)

    #Identify how much pink is in the image
        unique, counts = np.unique(mask, return_counts=True)

    #threshold for amount of pink needed in the image
        if counts.shape[0] == 2:
            colorthresholds[c]=counts[1] / counts[0]
    #check if pink was detected

    return dict(sorted(colorthresholds.items(), key=lambda item: item[1])) #-item=biggest first


image_path='/home/michael/code/Rob1412/rose_project/raw_data/flowers/magnolia/10599462_97cb6f005b_c.jpg'
print(multi_color_detect_img(cv2.imread(image_path)))
