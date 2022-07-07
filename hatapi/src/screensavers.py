import random
import time
import argparse
import pathlib
import os
from typing import List, Union

from hatapi.src.q_learner_saver import q_learner
from hatapi.src.q_learner_saver import chaser_env

file_dir_path = pathlib.Path(__file__).parent.resolve()
TABLES_DIR = pathlib.Path(f"{file_dir_path}{os.sep}q_learner_saver{os.sep}tables{os.sep}")


def run_screen_saver(sense, *args):
    parser = get_parser()
    namespace = parser.parse_args(args)

    if namespace.subcommand == "bounce":
        run_bouncy_saver(sense)
    elif namespace.subcommand == "q_learner":
        run_q_learning(sense, namespace)
    elif namespace.subcommand == "hacker":
        run_hacker_saver(sense, namespace)
    else:
        print("Please provide a subcommand")


def get_parser():
    parser = argparse.ArgumentParser("Run a screensaver")

    subparsers = parser.add_subparsers(dest="subcommand")

    add_bouncy_saver(subparsers)
    add_qlearner_parser(subparsers)
    add_hack_parser(subparsers)

    return parser


# BOUNCY

def add_bouncy_saver(subparsers):
    parser = subparsers.add_parser("bounce", help="Simple bouncing dot")


def run_bouncy_saver(sense):
    saver = ScreenSaverBounce(sense)
    saver.run()


class ScreenSaverBlob:
    TOTAL_DIRECTIONS = 8  # the 8 different directions of a grid move
    BOARD_DIMS = [8, 8]  # min max index allowed for x and y

    def __init__(self, loc, direction):
        self.pos = loc
        self.direction = direction

    def change_direction(self, change_chance=1.0):
        if change_chance > random.random():
            change = random.choice([-3, 3, 4])
            self.direction += change
            self.direction %= self.TOTAL_DIRECTIONS

    def move(self):
        if self.direction == 0:
            self.pos[1] -= 1
        elif self.direction == 1:
            self.pos[1] -= 1
            self.pos[0] += 1
        elif self.direction == 2:
            self.pos[0] += 1
        elif self.direction == 3:
            self.pos[0] += 1
            self.pos[1] += 1
        elif self.direction == 4:
            self.pos[1] += 1
        elif self.direction == 5:
            self.pos[0] -= 1
            self.pos[1] += 1
        elif self.direction == 6:
            self.pos[0] -= 1
        elif self.direction == 7:
            self.pos[0] -= 1
            self.pos[1] -= 1
        if self.pos[1] >= self.BOARD_DIMS[1] or self.pos[1] < 0 or \
                self.pos[0] >= self.BOARD_DIMS[0] or self.pos[0] < 0:
            self.change_direction()
            self.pos[0] = max(0, min(self.pos[0], 7))
            self.pos[1] = max(0, min(self.pos[1], 7))
            return True
        else:
            self.change_direction(0.05)
            return False


class ScreenSaverBounce:
    BACK_COLOR = (0, 0, 0)
    BLOB_COLOR = (255, 255, 255)

    def __init__(self, sense):
        self.sense = sense
        self.blobs = [ScreenSaverBlob([3, 3], random.randint(0, 7))]

    def run(self):
        try:
            print("Stop screensaver with  Ctrl-c")
            while True:
                for blob in self.blobs:
                    self.sense.set_pixel(*blob.pos, self.BACK_COLOR)
                    hit_wall = blob.move()
                    self.sense.set_pixel(*blob.pos, self.BLOB_COLOR)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.sense.clear()

    def make_new_blob(self, origin_blob):
        pass


# Q-LEARNER

def add_qlearner_parser(subparsers):
    parser = subparsers.add_parser("q_learner", help="Run a machine learning screensaver")
    parser.add_argument("-l", "--list_learners", help="List all learners that have been saved", action="store_true")
    parser.add_argument("-i", "--input", help="Name of a already learned learner. Default is None and will"
                                              " start a new learner", default=None)
    parser.add_argument("-e", "--show_every", help="Show every x generations what the learner looks like. Showing"
                                                   "all generations can mean very slow progression", default=100)
    parser.add_argument("-o", "--output", help="Name were the table is saved after shutdown. Leave it empty in order"
                                               "to not save the table.", default=None)
    return parser


def run_q_learning(sense, namespace):
    infile = namespace.input
    outfile = namespace.output
    show_every = namespace.show_every

    if namespace.list_learners is True:
        print("These are the available learners:")
        print_tables()
        return

    target_env = chaser_env.FindTargetEnvironment(sense, (8, 8))
    if infile is None and outfile is not None:
        if pathlib.Path(f"{TABLES_DIR}{os.sep}{outfile}.pickle").exists():
            total_ex = 1
            while True:
                answer = input("You are about to overwrite an existing learning table. Are you sure? (Y/N)")
                if answer.upper() == "Y":

                    break
                elif answer.upper() == "N":
                    return
                else:
                    print("Please type Y or N" + ("!" * total_ex))
                    total_ex += 1
    if infile is not None:
        try:
            learner = q_learner.QLearner.load(f"{TABLES_DIR}{os.sep}{infile}.pickle", sense)
            print(f"Loaded learner {infile}")
        except FileNotFoundError:
            print("No such input table available use one of:")
            print_tables()
            return
    else:
        learner = q_learner.QLearner(target_env, learning_rate=0.1, discount=0.9,
                                     action_mode="max", epsilon_decay=0.0001)
        print("Created new learner")
    try:
        print()
        print("Starting screensaver and learning...")
        print("Pres Ctrl-c to stop.")
        while True:
            learner.train(1, 100)
            if learner.total_generations % show_every == 0:
                learner.test(show_visual=True)
            else:
                learner.test(show_visual=False)
    except KeyboardInterrupt:
        if infile is not None:
            learner.save(f"{TABLES_DIR}{os.sep}{infile}.pickle")
            print(f"Saved table {infile}")
        elif outfile is not None:
            learner.save(f"{TABLES_DIR}{os.sep}{outfile}.pickle")
            print(f"Saved table {outfile}")


def print_tables():
    print(TABLES_DIR)
    paths = TABLES_DIR.rglob("*.pickle")
    for path in paths:
        print(path.stem)


# HACKER


def add_hack_parser(subparsers):
    parser = subparsers.add_parser("hacker", help="Green vertical lines")
    parser.add_argument("-rc", "--random_colors", help="Add this argument if you want random colors",
                        action="store_true")
    parser.add_argument("-s", "--speed", help="seconds between potential new spawns", default=HackerLines.DEFAULT_SPEED,
                        type=float)


def run_hacker_saver(sense, namespace):
    hacker_lines = HackerLines(sense, namespace.speed, namespace.random_colors)
    hacker_lines.run()


class HackerLines:

    MAX_DOTS = 8
    DEFAULT_SPEED = 0.2
    DOT_CHANGE = 0.2

    dots: List[Union["Dot", None]]

    def __init__(self, sense, speed, random_colors=False):
        self.speed = speed
        self.random_colors = random_colors
        self.sense = sense
        self.dots = [None for _ in range(8)]

    def run(self):
        try:
            print("Stop screensaver with Ctrl-c")
            while True:
                matrix = [(0, 0, 0) for _ in range(64)]
                for index, dot in enumerate(self.dots):
                    if dot is None:
                        continue
                    dot.move()
                    if not dot.alive():
                        self.dots[index] = None
                        continue
                    for pos, color in dot.get_pos_cols():
                        matrix[pos[0] + pos[1] * 8] = color
                self.make_dots()
                self.sense.set_pixels(matrix)
                time.sleep(self.speed)
        except KeyboardInterrupt:
            self.sense.clear()

    def make_dots(self):
        # this is stupid but the list is length 8 so who cares
        if len([d for d in self.dots if d is not None]) >= self.MAX_DOTS:
            return
        values = list(enumerate(self.dots))
        random.shuffle(values)
        for index, dot in values:
            if dot is not None:
                continue
            if random.random() < self.DOT_CHANGE:
                self.dots[index] = Dot(index, self.random_colors)
                break


class Dot:

    BASE_COLOR = (0, 255, 0)

    def __init__(self, x_pos, random_color):
        self.pos = [x_pos, 0]
        self.steps = random.randint(3, 5)
        self.color = [random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255])]\
            if random_color else self.BASE_COLOR

    def move(self):
        self.pos[1] += 1

    def get_pos_cols(self):
        for nr in range(self.steps):
            if 0 <= self.pos[1] - nr < 8:
                color = [int(self.color[0] - (self.color[0] / self.steps * nr)),
                         int(self.color[1] - (self.color[1] / self.steps * nr)),
                         int(self.color[2] - (self.color[2] / self.steps * nr))]
                yield (self.pos[0], self.pos[1] - nr), color

    def alive(self):
        return self.pos[1] < 8 + self.steps
