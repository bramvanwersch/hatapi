import argparse

from hatapi.src.utility import str_to_color


def show_message(sense, *cmd_arguments):
    parser = get_arg_parser()
    argument_class = parser.parse_args(cmd_arguments)
    sense.show_message(argument_class.message, argument_class.text_speed,
                       argument_class.text_color, argument_class.back_color)


def get_arg_parser():
    parser = argparse.ArgumentParser("Show a display message:")
    parser.add_argument("message")
    parser.add_argument("-s", "--text_speed", type=float, default=0.1)
    parser.add_argument("-c", "--text_color", type=str_to_color, default="255-255-255")
    parser.add_argument("-bc", "--back_color", type=str_to_color, default="0-0-0")
    return parser
