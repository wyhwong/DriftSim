import os
import yaml

def get_config():
    with open("config/config.yml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)

def load_base_waveform_params():
    return get_config()["base"]

def load_target_waveform_params():
    return get_config()["target"]

def load_match_params():
    return get_config()["match"]

def check_and_create_dir(directory):
    exist = os.path.isdir(directory)
    if not exist:
        os.mkdir(directory)
    return exist
