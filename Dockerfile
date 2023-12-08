FROM tensorflow/tensorflow

WORKDIR /prod

RUN apt-get update && apt-get install -y python3-opencv

COPY requirements_prod.txt requirements.txt
RUN pip install -r requirements.txt

COPY roserose4rose roserose4rose
COPY setup.py setup.py
RUN pip install .

# You can add --port $PORT if you need to set PORT as a specific env variable
CMD uvicorn roserose4rose.api.fast:app --host 0.0.0.0 --port $PORT
