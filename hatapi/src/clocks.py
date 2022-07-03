import datetime
import argparse
import time


def show_clock(sense, *cmd_arguments):
    parser = get_arg_parser()
    namespace = parser.parse_args(cmd_arguments)
    if namespace.clock_type in ("b", "binary"):
        show_binary_clock(sense, namespace.no_seconds)
    elif namespace.clock_type in ("a", "analog"):
        show_analog_clock(sense, namespace.no_seconds)
    elif namespace.clock_type in ("d", "digital"):
        show_digital_clock(sense, namespace.no_seconds)
    else:
        raise ValueError(f"Programmer failed to add option for {namespace.clock_type}")


def get_arg_parser():
    parser = argparse.ArgumentParser("Show a clock in binary or analog mode")
    parser.add_argument("-ct", "--clock_type", help="The type of clock shown. Either binary(b) or analog(a)",
                        choices=["binary", "b", "analog", "a", "d", "digital"], default="a")
    parser.add_argument("-ns", "--no_seconds", help="If seconds should be removed", action="store_false")
    return parser


def show_binary_clock(sense, show_seconds):
    matrix = []
    for rindex in range(8):
        for cindex in range(8):
            if rindex == 0 or rindex == 7 or cindex == 0 or cindex == 7:
                matrix.append([150, 0, 255])
            else:
                matrix.append([0, 0, 0])

    print("Ctrl-c to stop showing time")
    while True:
        try:
            set_binary_matrix(matrix, show_seconds)
            sense.set_pixels(matrix)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    sense.clear()


def set_binary_matrix(matrix, show_seconds):
    current_time = datetime.datetime.now()
    if show_seconds:
        set_binary(current_time.hour, 1 * 8 + 1, matrix, [255, 0, 0], 2)
        set_binary(current_time.minute, 3 * 8 + 1, matrix, [255, 150, 0], 2)
        set_binary(current_time.second, 5 * 8 + 1, matrix, [255, 255, 0], 2)
    else:
        set_binary(current_time.hour, 1 * 8 + 1, matrix, [255, 0, 0], 3)
        set_binary(current_time.minute, 4 * 8 + 1, matrix, [255, 150, 0], 3)


def set_binary(number, start_index, matrix, color, heigth):
    bin_number = f"{number:06b}"
    for index, val in enumerate(bin_number):
        if val == "1":
            for nr in range(heigth):
                matrix[start_index + index + nr * 8] = color
        else:
            for nr in range(heigth):
                matrix[start_index + index + nr * 8] = [0, 0, 0]


def show_analog_clock(sense, show_seconds):
    print("Ctrl-c to stop showing time")
    while True:
        try:
            # reset matrix
            matrix = [[0, 0, 0] for _ in range(8 * 8)]
            set_analog_matrix(matrix, show_seconds)
            sense.set_pixels(matrix)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    sense.clear()


def set_analog_matrix(matrix, show_seconds):
    current_time = datetime.datetime.now()
    set_notches(matrix, [150, 0, 255])
    if show_seconds:
        set_analog(current_time.second, matrix, [255, 255, 0], 60, 0)
    set_analog(current_time.minute, matrix, [255, 150, 0], 60, 0)
    # technically less correct but looks nicer
    set_analog(current_time.hour % 12 + current_time.minute / 60 / 2, matrix, [255, 0, 0], 12, 0)


def set_analog(number, matrix, color, max_, minus):
    start, end = start_end_coord(number, max_, minus)
    values = find_in_between(start, end)
    for value in values:
        matrix[value[0] + value[1] * 8] = color


def set_notches(matrix, color):
    for nr in range(12):
        coord, _ = start_end_coord(nr, 12)
        matrix[coord[0] + coord[1] * 8] = color


def start_end_coord(number, max_, minus=0):
    step_size = 28 / max_
    circular_index = round(step_size * number)
    if circular_index < 4:
        x, y = (4 + circular_index, 0 + minus)
        cx, cy = (4, 3)
    elif 4 <= circular_index < 11:
        x, y = (7 - minus, (circular_index - 2) - 1)
        if y < 4:
            cx, cy = (4, 3)
        else:
            cx, cy = (4, 4)
    elif 11 <= circular_index < 18:
        x, y = (8 - (circular_index - 9), 7 - minus)
        if x > 3:
            cx, cy = (4, 4)
        else:
            cx, cy = (3, 4)
    elif 18 <= circular_index < 25:
        x, y = (0 + minus, 8 - (circular_index - 16))
        if y > 3:
            cx, cy = (3, 4)
        else:
            cx, cy = (3, 3)
    else:
        x, y = (min(circular_index - 24, 3), 0 + minus)
        cx, cy = (3, 3)
    return (x, y), (cx, cy)


def find_in_between(start, end):

    change_coords = {start, end}
    delta_x = abs(start[0] - end[0])
    delta_y = abs(start[1] - end[1])
    if delta_y > delta_x:
        if start[1] > end[1]:
            temp = start
            start = end
            end = temp
        # change in y per x
        try:
            change = (start[0] - end[0]) / (start[1] - end[1])
        except ZeroDivisionError:
            change = 0
        x, y = start
        for _ in range(end[1] - start[1]):
            x += change
            y += 1
            change_coords.add((round(x), round(y)))
    else:
        if start[0] > end[0]:
            temp = start
            start = end
            end = temp
        # change in x per y
        try:
            change = (start[1] - end[1]) / (start[0] - end[0])
        except ZeroDivisionError:
            change = 0
        x, y = start
        for _ in range(end[0] - start[0]):
            x += 1
            y += change
            change_coords.add((round(x), round(y)))
    return change_coords


def show_digital_clock(sense, show_seconds):
    while True:
        current_time = datetime.datetime.now()
        if show_seconds:
            string_time = f"{current_time.hour}:{current_time.minute}:{current_time.second}"
        else:
            string_time = f"{current_time.hour}:{current_time.minute}"
        sense.show_message(string_time)
        time.sleep(1)
