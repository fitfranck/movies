#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y moviespred || :
	@pip install -e .
