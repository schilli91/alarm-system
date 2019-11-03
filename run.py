#!/usr/bin/env python3


import configparser
import os.path
import threading
from datetime import datetime
from time import sleep

import requests
from gpiozero import InputDevice

from call import make_call
from config.config import CONFIG_DIR

if not os.path.isfile(CONFIG_DIR):
    raise Exception("The config path is invalid!")

config = configparser.ConfigParser()

URL = 'http://www.google.com/'
TIMEOUT = 5


def schedule_connection_check(interval=60):
    try:
        _ = requests.get(URL, timeout=TIMEOUT)
        with open('last_poll.txt', 'w+') as poll_file:
            now = datetime.now()
            poll_file.write(now.strftime('%d.%m.%Y %H:%M:%S'))
    except requests.ConnectionError:
        return
    threading.Timer(interval, schedule_connection_check).start()


if __name__ == "__main__":
    input_device = InputDevice(4, True)
    schedule_connection_check(interval=10800)

    while True:
        config.read(CONFIG_DIR)
        if input_device.is_active:
            make_call()
            sleep(int(config["DEFAULT"]["SLEEP_AFTER_CALL"]))
        sleep(1)
