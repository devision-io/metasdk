import os

SAMPLES_DIR = os.path.dirname(os.path.abspath(__file__)) + "/samples"


def get_sample_fn(file_name):
    return SAMPLES_DIR + "/" + file_name
