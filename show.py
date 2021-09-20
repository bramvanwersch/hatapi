from sys import argv
import argparse

from sense_hat import SenseHat


COLORS = {
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "yellow": [255, 255, 0],
    "magenta": [255, 0, 255],
    "cyan": [0, 255, 255],
    "white": [255, 255, 255],
    "light grey": [150, 150, 150],
    "grey": [100, 100, 100],
    "black": [0, 0, 0],
}

def main():
    args = argv[1:]
    parser = get_arg_parser()
    argument_class = parser.parse_args(args)
    show_message(argument_class.message, argument_class.text_speed,
                 argument_class.text_color, argument_class.back_color)
    

def get_arg_parser():
    parser = argparse.ArgumentParser("Show a display message:")
    parser.add_argument("message")
    parser.add_argument("-s", "--text_speed", type=float, default=0.1)
    parser.add_argument("-c", "--text_color", type=str_color, default="255-255-255")
    parser.add_argument("-bc", "--back_color", type=str_color, default="0-0-0")
    return parser
   
   
def str_color(color_str):
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


def show_message(message, speed, text_color, back_color):
    sense = SenseHat()
    sense.low_light = True
    sense.set_rotation(180)
    sense.show_message(message, speed, text_color, back_color)
    sense.clear()


if __name__ == "__main__":
    main()
    
    