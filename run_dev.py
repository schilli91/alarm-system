#!/usr/bin/env python3
from gpiozero import Button, InputDevice
from time import sleep
from call import make_call

if __name__ == "__main__":
    # input = InputDevice(4, True)
    button = Button(3)
    print(button)

    while True:
        # if input.is_active:
        if button.is_pressed:
            print('pressed')
            make_call(is_dev=True)
        # else:
        # print('.')
        sleep(1)
