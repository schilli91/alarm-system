#!/usr/bin/env python3
import os.path
from time import sleep

import configparser
from gpiozero import InputDevice

from call import make_call
from config.config import CONFIG_DIR

if not os.path.isfile(CONFIG_DIR):
    raise Exception("The config path is invalid!")

config = configparser.ConfigParser()

if __name__ == "__main__":
    input = InputDevice(4, True)

    while True:
        config.read(CONFIG_DIR)
        if input.is_active:
            make_call()
            sleep(int(config["DEFAULT"]["SLEEP_AFTER_CALL"]))
        sleep(1)
