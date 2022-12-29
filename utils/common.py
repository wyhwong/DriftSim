#!/usr/bin/env python3
import os
import yaml

def load_base():
    with open("config/base.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)

def load_target():
    with open("config/target.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)

def load_match():
    with open("config/match.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)

def check_and_create_dir(directory):
    exist = os.path.isdir(directory)
    if not exist:
        os.mkdir(directory)
    return exist
