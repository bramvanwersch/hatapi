from constants import NUMBERS, COLORS


def show_numbers(sense, number1, number2):
    """Set two numbers on the sensehat"""
    number_matrix = NUMBERS[number1]
    for x_index, x in enumerate([0, 1, 2, 3]):
        for y in range(8):
            color = (0, 0, 0) if number_matrix[y][x] == 0 else (255, 255, 255)
            sense.set_pixel(x, y, color)

    number_matrix = NUMBERS[number2]
    for x_index, x in enumerate([0, 1, 2, 3]):
        for y in range(8):
            color = (0, 0, 0) if number_matrix[y][x] == 0 else (255, 255, 255)
            sense.set_pixel(x + 4, y, color)


def str_to_color(color_str):
    """Read a color in format R-G-B as or as a string containing a predefined color as a list of rgb values"""
    values = color_str.split("-")
    if len(values) != 3:
        if values[0] in COLORS:
            return COLORS[values[0]]
        argparse.ArgumentError("Color format should be: R-G-B")
    try:
        for index in range(len(values)):
            int_val = int(values[index])
            if 0 > int_val > 255:
                argparse.ArgumentError(f"Invalid color arg {values[index]}. Needs to be between 0-255")
            values[index] = int(values[index])
    except ValueError:
        argparse.ArgumentError(f"Invalid color arg {values[index]}. Expected an Integer")
    return values
