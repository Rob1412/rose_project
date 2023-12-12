import numpy as np

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

def predict(contents,model):

    # # Use dumps() to make it serialized

    # # Open a file and use dump()
    # with open('file.pkl', 'wb') as file:

    #     # A new file will be created
    #     pickle.dump(contents, file)

    img = Image.open(BytesIO(contents))
    img = img.resize((128,128)) # resize image
    X_new = img_to_array(img).reshape((-1,128,128,3)) # convert image to np array

    probs = model.predict(X_new, verbose=0) # make prediction

    label = np.argmax(probs) # take most likely label (i.e. species)

    return (flower_labels[label], float(probs[0,label]))


######## IGNORE BELOW HERE (FOR LOCAL VERSION ONLY) ########

# from tensorflow.keras.preprocessing.image import load_img

# img_path = "/home/rob/code/Rob1412/rose_project/raw_data/sunf.jpg"

# img = load_img(img_path).resize((128,128))


# import pickle
# # Open the file in binary mode
# with open('/home/michael/code/Rob1412/rose_project/file.pkl', 'rb') as file:

#     # Call load method to deserialze
#     contents = pickle.load(file)

# print(predict(contents))
