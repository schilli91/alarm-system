#!/usr/bin/env python3
from gpiozero import InputDevice
from time import sleep
from call import make_call

if __name__ == "__main__":
    input = InputDevice(4, True)

    while True:
        if input.is_active:
            make_call()
        sleep(1)
