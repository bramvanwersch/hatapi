#!/usr/bin/env python

from sense_hat import SenseHat
from sys import argv

from measure_display import show_temp, show_humid, show_value_bars
from show_message import show_message
from snake import run_snake
from screen_savers import run_screen_saver
from run_q_screensaver import run_learning


def main():
    # mapping for requests
    request_mapping = {
        "bars": show_value_bars,
        "t": show_temp,
        "temp": show_temp,
        "temperature": show_temp,
        "h": show_humid,
        "humid": show_humid,
        "humidity": show_humid,
        "m": show_message,
        "message": show_message,
        "snake": run_snake,
        "ss": run_screen_saver,
        "screensaver": run_screen_saver,
        "qs": run_learning,
        "qscreensaver": run_learning
    }

    sense = SenseHat()
    sense.set_rotation(180)
    sense.low_light = True
    # make sure to always clear even if no valid arguments are supplied
    sense.clear()
    try:
        request = argv[1]
        other_args = argv[2:]
    except IndexError:
        print(f"Please request a function. Choose one of: {', '.join(request_mapping.keys())}")
        return

    if request not in request_mapping:
        print(f"Unknown request: {request}. Choose one of: {', '.join(request_mapping.keys())}")
        return

    try:
        if len(other_args) == 1:
            # or strings become individual args
            request_mapping[request](sense, other_args)
        else:
            request_mapping[request](sense, *other_args)
    except Exception as e:
        sense.clear()
        raise e
    sense.clear()


if __name__ == '__main__':
    main()
