import time

from hatapi.src.utility import show_numbers


def show_value_bars(sense, display_time=5):
    monitor = ValueBarShow(sense)
    monitor.set_humidity_values()
    monitor.set_temperature_values()
    _wait_display_time(display_time)


def show_temp(sense, display_time=5):
    temp_value = round(sense.get_temperature())
    n1, n2 = divmod(temp_value, 10)
    show_numbers(sense, n1, n2)
    _wait_display_time(display_time)


def show_humid(sense, display_time=5):
    humid_value = round(sense.get_humidity())
    n1, n2 = divmod(humid_value, 10)
    show_numbers(sense, n1, n2)
    _wait_display_time(display_time)


def _wait_display_time(display_time):
    try:
        time.sleep(int(display_time))
    except ValueError:
        print("Expected an integer for show_time.")


class ValueBarShow:
    TEMP_RANGE = [0, 50]
    TEMP_COLORS = [(int(255 / 16 * i), 0, int(255 - 255 / 16 * i)) for i in range(16)]
    HUMIDITY_RANGE = [0, 75]
    HUMID_COLORS = [(0, int(255 / 16 * i), int(255 - 255 / 16 * i)) for i in range(16)]

    def __init__(self, sense):
        self.sense = sense

    def set_humidity_values(self):
        frac_humid = self.sense.get_humidity() / self.HUMIDITY_RANGE[1]
        colors = [(0, 0, 0) for _ in range(16)]
        for index in range(int(frac_humid * 16)):
            colors[index] = self.HUMID_COLORS[index]

        for x_index, x in enumerate([5, 6]):
            for y in range(8):
                self.sense.set_pixel(x, y, colors[x_index * 8 + (7 - y)])

    def set_temperature_values(self):
        frac_temp = self.sense.get_temperature() / self.TEMP_RANGE[1]
        colors = [(0, 0, 0) for _ in range(16)]
        for index in range(int(frac_temp * 16)):
            colors[index] = self.TEMP_COLORS[index]

        for x_index, x in enumerate([1, 2]):
            for y in range(8):
                self.sense.set_pixel(x, y, colors[x_index * 8 + (7 - y)])
