#!/usr/bin/env python3


from time import sleep

from gpiozero import Button

from call import make_call
from run import schedule_connection_check

if __name__ == "__main__":
    # input = InputDevice(4, True)
    button = Button(23)
    print(button)
    schedule_connection_check(interval=60)

    while True:
        # if input.is_active:
        if button.is_pressed:
            print('pressed')
            make_call(is_dev=True)
        # else:
        # print('.')
        sleep(1)
