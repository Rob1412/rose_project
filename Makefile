##### Prediction API - - - - - - - - - - - - - - - - - - - - - - - - -

run_api:
	uvicorn fast_api.api:app --reload

##### Docker - - - - - - - - - - - - - - - - - - - - - - - - -

docker_build:
	docker build -t RoseRose4Rose .

docker_run:
	docker run -p 8000:8000 --name api RoseRose4Rose

##### GCP - - - - - - - - - - - - - - - - - - - - - - - - -

GCP_PROJECT_ID=XXX

DOCKER_IMAGE_NAME='RoseRose4Rose'

# https://cloud.google.com/storage/docs/locations#location-mr
GCR_MULTI_REGION='EUROPE-WEST2'

# https://cloud.google.com/compute/docs/regions-zones#available
REGION='europe-west2-a'

build_gcr_image:
	docker build -t $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME) .

build_gcr_image_m1:
	docker build --platform linux/amd64 -t $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME) .

run_gcr_image:
	docker run -e PORT=8000 -p 8080:8000 $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME)

push_gcr_image:
	docker push $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME)

gcr_deploy:
	gcloud run deploy --image $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME) --platform managed --region $(REGION)

----------------------------------------------------

gar_creation:
  gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev
  gcloud artifacts repositories create ${GAR_REPO} --repository-format=docker \
  --location=${GCP_REGION} --description="Repository for storing ${GAR_REPO} images"

docker_build:
	docker build -t ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod .

docker_push:
	docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod

docker_run:
  docker run -e PORT=8000 -p 8000:8000 --env-file .env ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod

docker_interactive:
  docker run -it --env-file .env ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod /bin/bash

docker_deploy:
  gcloud run deploy --image ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod --memory ${GAR_MEMORY} --region ${GCP_REGION} --env-vars-file .env.ta.yaml