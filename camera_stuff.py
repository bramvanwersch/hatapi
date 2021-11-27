from picamera import PiCamera
import time


def take_photo(_, name):
    camera = PiCamera()
    camera.resolution = (800, 600)
    camera.rotation = 270
    current_file = __file__
    current_dir = current_file.rsplit('/', 1)[0]
    camera.capture(f"{current_dir}/images/{name}.png")
