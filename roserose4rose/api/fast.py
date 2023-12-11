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

@app.post('/upload_image')
async def receive_image(img: UploadFile=File(...)):
    ### Receiving and decoding the image
    contents = await img.read()
    class_response=predict(contents)
    pred_class=class_response[0]
    pred_prob=round(class_response[1]*100)

    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray
    colour_response=find_pink_imported_img(cv2_img)
    returnval={'pred_class':pred_class,
               'pred_prob':pred_prob,
               'how_much_pink':colour_response}

    ### Encoding and responding with the image
    #im = cv2.imencode('.png', annotated_img)[1] # extension depends on which format is sent from Streamlit
    #Response(content=im.tobytes(), media_type="image/png")
    return returnval

@app.get("/")
def root():
    return dict(greeting="Hello")
