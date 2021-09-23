import random
import time


def run_screen_saver(sense):
    saver = ScreenSaver1(sense)
    saver.run()


class ScreenSaver1Blob:
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


class ScreenSaver1:
    BACK_COLOR = (0, 0, 0)
    BLOB_COLOR = (255, 255, 255)

    def __init__(self, sense):
        self.sense = sense
        self.blobs = [ScreenSaver1Blob([3, 3], random.randint(0, 7))]

    def run(self):
        try:
            print("Stop screensaver with <Ctrl + c>")
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




