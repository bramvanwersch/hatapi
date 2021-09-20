from sense_hat import SenseHat, ACTION_PRESSED
import random
import time
import termios
import fcntl
import sys
import os


def run_snake(sense):
    game = Snake(sense)
    game.run()


class Snake:
    BOARD_DIMS = [8, 8]
    COLORS = {
        "apple": [255, 0, 0],
        "snake": [0, 255, 0],
        "head": [0, 255, 255],
        "back": [0, 0, 0]
    }

    def __init__(self, sense):
        self._snake = [[4, 4], [3, 4]]
        self.sense = sense
        self._apple_location = [0, 0]
        self._place_apple()
        self.going = True
        self.speed = [1, 0]
        self.total_apples = 0

        # set the joystick controls
        self.sense.stick.direction_up = self._move_down
        self.sense.stick.direction_down = self._move_up
        self.sense.stick.direction_left = self._move_right
        self.sense.stick.direction_right = self._move_left

    def _move_up(self, event):
        if event == "key" or event.action == ACTION_PRESSED:
            self.speed[1] = -1
            self.speed[0] = 0

    def _move_down(self, event):
        if event == "key" or event.action == ACTION_PRESSED:
            self.speed[1] = 1
            self.speed[0] = 0

    def _move_left(self, event):
        if event == "key" or event.action == ACTION_PRESSED:
            self.speed[1] = 0
            self.speed[0] = -1

    def _move_right(self, event):
        if event == "key" or event.action == ACTION_PRESSED:
            self.speed[1] = 0
            self.speed[0] = 1

    def _process_key(self, key):
        if key == "w":
            self._move_up("key")
        elif key == "s":
            self._move_down("key")
        elif key == "a":
            self._move_left("key")
        elif key == "d":
            self._move_right("key")

    def _place_apple(self):
        # random until location not on snake --> kinda slow but does not matter in this case
        while True:
            x, y = random.randint(0, 7), random.randint(0, 7)
            matched = False
            for segment in self._snake:
                if [x, y] == segment:
                    matched = True
                    break
            if not matched:
                self._apple_location = [x, y]
                break
        self.sense.set_pixel(*self._apple_location, self.COLORS["apple"])

    def run(self):
        # to get keyboard input tyty :)
        #  https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-termina
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        while self.going:
            c = sys.stdin.read(1)
            if c:
                self._process_key(c)
            self.move()
            self.check_collision()
            time.sleep(0.2)
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        self.sense.clear()
        self.sense.show_message(f"S: {self.total_apples}")

    def move(self):
        head_location = self._snake[0].copy()
        self._snake[0][0] += self.speed[0]
        self._snake[0][1] += self.speed[1]
        if self._snake[0][1] >= self.BOARD_DIMS[1] or self._snake[0][1] < 0 or\
                self._snake[0][0] >= self.BOARD_DIMS[0] or self._snake[0][0] < 0:
            self.going = False
            print("lost the game")
            return
        self._move_snake_body(head_location)

    def _move_snake_body(self, prev_segment):
        self.sense.set_pixel(*self._snake[0], self.COLORS["head"])
        for index in range(1, len(self._snake)):
            current_segment = self._snake[index]
            self.sense.set_pixel(*current_segment, self.COLORS["back"])
            self._snake[index] = prev_segment
            self.sense.set_pixel(*self._snake[index], self.COLORS["snake"])
            prev_segment = current_segment

    def check_collision(self):
        snake_head = self._snake[0]
        if snake_head == self._apple_location:
            self._place_apple()
            self.total_apples += 1
            self._snake.append(self._snake[-1].copy())
            return
        for part in self._snake[1:]:
            if part == snake_head:
                self.going = False
                print("lost the game")
                return
