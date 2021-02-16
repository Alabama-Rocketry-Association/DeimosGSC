from ruamel.yaml import YAML
from SRC.zoomm9 import z9c
import os
import datetime

#global variables
global LOGGING_DIR
global WORKING_DIR
global CONFIG_PATH
global RADIOCONFIG
global CONFIG
CONFIG = dict()
LOGGIN_DIR = None #logging directory
RADIOCONFIG = dict.fromkeys(["DEVICE", "BAUDRATE"])           
WORKING_DIR = os.getcwd()   #current directory
CONFIG_PATH = "config.yaml" #yaml style config file

#macros
current_time = lambda : datetime.datetime.now().strptime("%d:%m:%y-%H:%M:%S")

#helper functions
def load(config_path = CONFIG_PATH):
    global CONFIG
    reader = YAML()
    with open(config_path, "r") as f:
        config = reader.load(f)
        CONFIG = config
    return




