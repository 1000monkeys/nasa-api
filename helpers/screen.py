import sys

import pygame

class Screen:
    def handle_events(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

    def draw(self) -> None:
        """Empty draw needed because all screens need this method
        """
        pass