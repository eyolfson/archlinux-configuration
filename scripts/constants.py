import os

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
HOST_SPECIFIC_DIR = os.path.join(BASE_DIR, 'host-specific')
