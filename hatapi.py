from sense_hat import SenseHat
from sys import argv

from measure_display import show_temp, show_humid, show_value_bars


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
    }

    try:
        request = argv[1]
        other_args = argv[2:]
    except IndexError:
        print(f"Please request a function. Choose one of: {', '.join(request_mapping.keys())}")
        return

    if request not in request_mapping:
        print(f"Unknown request: {request}. Choose one of: {', '.join(request_mapping.keys())}")
        return

    sense = SenseHat()
    sense.set_rotation(180)
    sense.low_light = True
    try:
        request_mapping[request](sense, *other_args)
    except Exception as e:
        sense.clear()
        raise e
    sense.clear()


class ScreenSaverBlob:
    def __init__(self, pos):
        self.pos = loc


class ScreenSaver:
    def __init__(self):
        self.field = [(0, 0, 0) for _ in range(8)]


if __name__ == '__main__':
    main()
