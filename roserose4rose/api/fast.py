# $WIPE_BEGIN

# $WIPE_END


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from roserose4rose.color_detection.color_detection import find_pink_imported_img
from roserose4rose.flower_classificator.flower_classifier import predict
app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2


@app.post('/upload_image')
async def receive_image(img: UploadFile=File(...)):
    ### Receiving and decoding the image
    contents = await img.read()
    class_response=predict(contents)
    pred_class=class_response[0]
    pred_prob=round(class_response[1]*100)
    returnval=f'This is a {pred_class} with probability {pred_prob}%'
    if pred_class=="rose":
        nparr = np.fromstring(contents, np.uint8)
        cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray
        colour_response=find_pink_imported_img(cv2_img)

        if not colour_response:
            returnval=f'This is a rose with probability {pred_prob}% but not in colour pink'
        else:
            returnval=f'This is a rose with probability {pred_prob}% and it is pink'



    ### Encoding and responding with the image
    #im = cv2.imencode('.png', annotated_img)[1] # extension depends on which format is sent from Streamlit
    #Response(content=im.tobytes(), media_type="image/png")
    return returnval

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
