#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y moviespred || :
	@pip install -e .


#################### TEST SETUP ###################
test_bucket_access:
	@python tests/gcs/test_gcs_upload.py
