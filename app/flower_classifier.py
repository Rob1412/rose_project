import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

from PIL import Image
from io import BytesIO

flower_labels = {
    0: 'astilbe',
    1: 'bellflower',
    2: 'black_eyed_susan',
    3: 'calendula',
    4: 'california_poppy',
    5: 'carnation',
    6: 'common_daisy',
    7: 'coreopsis',
    8: 'daffodil',
    9: 'dandelion',
    10: 'iris',
    11: 'magnolia',
    12: 'rose',
    13: 'sunflower',
    14: 'tulip',
    15: 'water_lily'
}

def predict(contents):

    model = load_model("./models/mobilenet_tl_model.h5")    # CHECK DIRECTORY!

    img = Image.open(BytesIO(contents))

    img = img.resize((128,128)) # resize image

    X_new = img_to_array(img).reshape((-1,128,128,3)) # convert image to np array

    probs = model.predict(X_new, verbose=0) # make prediction

    label = np.argmax(probs) # take most likely label (i.e. species)

    return (flower_labels[label], probs[0,label])


######## IGNORE BELOW HERE (FOR LOCAL VERSION ONLY) ########

# from tensorflow.keras.preprocessing.image import load_img

# img_path = "/home/rob/code/Rob1412/rose_project/raw_data/sunf.jpg"

# img = load_img(img_path).resize((128,128))