from pathlib import Path
import time
from urllib.parse import urlparse
from urllib.request import urlopen

import pygame


class Image():
    def __init__(self, screen, file_name):
        self.screen = screen
        self.file_name = file_name

        try:
            self.image = pygame.image.load("images\\" + self.file_name)
        except FileNotFoundError or PermissionError:
            time.sleep(500)
            print(self.file_name)
            self.image = pygame.image.load("images\\" + self.file_name)

        x, y = self.image.get_size()
        rx = 924 / x
        ry = 636 / y
        ratio = rx if rx < ry else ry
        self.image = pygame.transform.scale(self.image, (int(x*ratio), int(y*ratio)))

        height = self.image.get_height()
        width = self.image.get_width()

        #print("Height: " + str(height) + " width: " + str(width))

        self.pos = (100 + (924 / 2) - (width / 2), 150 + (636 / 2) - (height / 2))

    def draw(self):
        self.screen.blit(self.image, self.pos)

    def handle_events(self, events):
        pass
