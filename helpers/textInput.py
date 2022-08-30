from __future__ import annotations
import time

from typing import Tuple
import pygame
from helpers.screen import Screen
from helpers.UIElement import UIElement


class TextInput(UIElement):
    def __init__(self, screen: Screen, text: str, position: Tuple, text_color: str, background_color: Tuple=None, border_color: Tuple=None, border_width: int=None, max: int=None, callback_function: function=None):
        """Allows for text input into a textbox

        :param screen: The screen to draw to
        :type screen: Screen
        :param text: The text to initialize the textinput with, Empty for no text
        :type text: str
        :param position: X, Y Position of the text input, Top left corner
        :type position: Tuple
        :param text_color: Color of the text
        :type text_color: str
        :param background_color: Background color behind the text, defaults to None
        :type background_color: Tuple, optional
        :param border_color: Border color around the background, defaults to None
        :type border_color: Tuple, optional
        :param border_width: Size of the border around the backgroundf, defaults to None
        :type border_width: int, optional
        :param max: Maximum input size, defaults to None
        :type max: int, optional
        """
        self.screen = screen
        self.text = text
        self.position = position
        self.text_color = text_color
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.max = max
        self.callback_function = callback_function

        self.changed_text = False
        self.font = pygame.font.SysFont("arial", 48)
        width, height = self.font.size(self.text)
        if self.border_color != None and self.border_width != None:
            self.border_rect = pygame.Rect(
                self.position[0] - self.border_width,
                self.position[1] - self.border_width,
                width + 20 + self.border_width * 2 + 10,
                height + self.border_width * 2
            )
        self.rect = pygame.Rect(self.position[0], self.position[1], width + 20 + 10, height)
        
        self.background_color = background_color
        self.cursor = self.font.render("|", False, self.text_color)


    def get_rect(self) -> pygame.Rect:
        """Returns the rect which contains the position and size of the button. The background rect.

        :return: position dictionary with 4 values, first 2 being X/Y and next 2 being width/height
        :rtype: pygame.Rect
        """
        return self.rect

    def get_input(self) -> str:
        """Gets the text which has ben input into this textinput

        :return: The text which the user has input
        :rtype: str
        """
        return self.text

    def set_input(self, text: str) -> None:
        """Sets the text to the passed parameter

        :param text: Sets the text to the parameter
        :type text: str
        """
        self.text = text

    def update_size(self) -> None:
        """Changes the size of the textinput after text has been input or removed
        """
        width, height = self.font.size(self.text)
        if self.border_color != None and self.border_width != None:
            self.border_rect = pygame.Rect(
                self.position[0] - self.border_width,
                self.position[1] - self.border_width,
                width + 20 + self.border_width * 2,
                height + self.border_width * 2
            )
        self.rect = pygame.Rect(self.position[0], self.position[1], width + 20, height)

    def draw(self):
        """Draw method usually called in the screen to draw the textinput
        """
        super().draw()

        self.update_size()

        if self.border_color != None and self.border_width != None:
            pygame.draw.rect(self.screen, self.border_color, self.border_rect)
        
        if self.background_color != None:
            pygame.draw.rect(self.screen, self.background_color, self.rect)

        text_img = self.font.render(self.text, False, self.text_color)
        self.screen.blit(text_img, (self.rect.x + 10, self.rect.y))
        if time.time() % 1 > 0.5:
            self.screen.blit(self.cursor, (self.rect.x + self.rect.width - 10, self.rect.y - 5))

    def handle_events(self, events: pygame.EventList) -> None:
        """Handles events passed here from the screen

        :param events: Events to check
        :type events: pygame.EventList
        """
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key:
                    if event.unicode.isdigit() and len(self.text) < self.max:
                        if not self.changed_text:
                            self.changed_text = True
                            self.text = str(event.unicode)
                        else:
                            self.text += event.unicode
