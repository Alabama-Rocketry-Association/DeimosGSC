import async
import pandas as pd
import datetime
import os
from ruamel.yaml import YAML






class GSC(object):

    def __init__(self):
        super().__init__()






def main(logging_dir = f"data-{current_date}"):
    global LOGGIN_DIR
    LOGGIN_DIR = os.mkdir(logging_dir)



if __name__ == "__main__":
    main()