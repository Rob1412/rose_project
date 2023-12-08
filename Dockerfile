FROM python:3.10.6-buster

WORKDIR /roserose4rose

# libraries required by OpenCV
#RUN apt-get update
#RUN apt-get install \
#  'ffmpeg'\
#  'libsm6'\
#  'libxext6'  -y

COPY requirements.txt .
COPY setup.py .
RUN pip install -r requirements.txt

COPY /roserose4rose /roserose4rose

RUN pip install -e .
RUN apt-get update
RUN apt install -y libgl1-mesa-glx



COPY . .

# You can add --port $PORT if you need to set PORT as a specific env variable
#CMD uvicorn fast_api.api:app --host 0.0.0.0 --port $PORT
#PORT=8080
CMD uvicorn roserose4rose.api.fast:app --reload --host 0.0.0.0 --port $PORT
