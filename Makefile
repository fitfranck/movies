#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y moviespred || :
	@pip install -e .

#################### CHECK DATA ###################
count_train_images:
	@ find images_train/ -type f -iname "*.jpg" | wc -l

size_train_images:
	@ du -sh images_train

empty_train_images:
	@ find images_train -type f -empty

#################### TEST SETUP ###################
test_bucket_access:
	@python tests/gcs/test_gcs_upload.py

#################### API ###################
run_api:
	@uvicorn api.main:app --reload

#################### API ###################

run_streamlit:
	@streamlit run streamlit/streamlit_app.py
#################### DOCKER ###################
docker_build:
	@docker build -t ${GCP_MULTI_REGION}/${GCP_PROJECT}/${IMAGE_NAME} .

docker_run:
	@docker run -e PORT=8000 -p 8080:8000 ${GCP_MULTI_REGION}/${GCP_PROJECT}/${IMAGE_NAME}

docker_push:
	@docker push ${GCP_MULTI_REGION}/${GCP_PROJECT}/${IMAGE_NAME}

run_deploy:
	@gcloud run deploy --image ${GCP_MULTI_REGION}/${GCP_PROJECT}/${IMAGE_NAME} --memory 2Gi --region ${GCP_REGION}
