import async
import pandas as pd
import datetime
import os
from ruamel.yaml import YAML

LOGGIN_DIR = None           #logging directory
WORKING_DIR = os.getcwd()   #current directory
CONFIG_PATH = "config.yaml" #yaml style config file
global LOGGING_DIR
global WORKING_DIR
global CONFIG_PATH


current_date = lambda : datetime.datetime.now().strptime("%d:%m:%y-%H:%M:%S")

class GSC(object):

    def __init__(self):
        super().__init__()






def main(logging_dir = f"data-{current_date}"):
    global LOGGIN_DIR
    LOGGIN_DIR = os.mkdir(logging_dir)



if __name__ == "__main__":
    main()