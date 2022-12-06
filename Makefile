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
