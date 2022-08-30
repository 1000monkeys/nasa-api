from __future__ import annotations
from types import FunctionType
from typing import Tuple

from helpers.screen import Screen
            
import pygame

from helpers.UIElement import UIElement

class Button(UIElement):
    def __init__(self, screen: Screen, text: str, position: Tuple, text_color: Tuple, background_color: Tuple=None, border_color: Tuple=None, border_size: int=0, font_size: int=36, padding: int=0, callback_function: FunctionType=None) -> None:
        """The initializer of the button which sets it up with the data.

        :param screen: Screen to draw to in the draw method
        :type screen: Screen
        :param text: Text inside the button
        :type text: str
        :param position: The position of the button, top left corner
        :type position: Tuple
        :param text_color: Color of the text, RGB value
        :type text_color: Tuple
        :param background_color: background color of the button, behind the text, RGB value, defaults to None
        :type background_color: Tuple, optional
        :param border_color: border color around the background colorm, RGB value, defaults to None
        :type border_color: Tuple, optional
        :param border_size: Size of the border with color of border_color, defaults to 0
        :type border_size: int, optional
        :param font_size: Size of the font, defaults to 36
        :type font_size: int, optional
        :param padding: padding inside the button, makes background_color are larger, defaults to 0
        :type padding: int, optional
        :param callback_function: Function to call after mouseclick on button, defaults to None
        :type callback_function: FunctionType, optional
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text = text
        self.position = position
        self.text_color = text_color
        self.background_color = background_color
        self.border_color = border_color
        self.border_size = border_size
        self.font_size = font_size
        self.padding = padding
        self.callback_function = callback_function

        self.font = pygame.font.SysFont("arial", self.font_size)
        self.font_width, self.font_height = self.font.size(self.text)

        self.normal_rect = pygame.Rect(
            self.position[0],
            self.position[1],
            self.font_width + self.padding * 2,
            self.font_height + self.padding * 2
        )
        self.normal_border_rect = pygame.Rect(
            self.position[0] - self.padding - self.border_size,
            self.position[1] - self.padding - self.border_size,
            self.font_width + self.padding * 4 + self.border_size * 2,
            self.font_height + self.padding * 4 + self.border_size * 2
        )

        self.larger_rect = pygame.Rect(
            self.position[0] - self.padding * 2,
            self.position[1] - self.padding * 2,
            self.font_width + self.padding * 6,
            self.font_height + self.padding * 6
        )
        self.larger_border_rect = pygame.Rect(
            self.position[0] - self.padding * 3 - self.border_size,
            self.position[1] - self.padding * 3 - self.border_size,
            self.font_width + self.padding * 8 + self.border_size * 2,
            self.font_height + self.padding * 8 + self.border_size * 2
        )

        self.text_rendered = self.font.render(
            self.text,
            True,
            self.text_color,
            self.background_color
        )
        
        self.rect = self.normal_rect
        self.border_rect = self.normal_border_rect
        self.text_rect = self.text_rendered.get_rect()
        self.text_rect.center = self.normal_rect.center

    def get_rect(self) -> pygame.Rect:
        """Returns the rect which contains the position and size of the button. The background rect.

        :return: position dictionary with 4 values, first 2 being X/Y and next 2 being width/height
        :rtype: pygame.Rect
        """
        return self.rect

    def set_center_position(self, position: Tuple) -> None:
        """Sets the button with the center of the rectangle on the position passed as argument

        :param position: The position to center the button on
        :type position: Tuple
        """
        self.normal_rect.center = position
        self.normal_border_rect.center = position
        self.larger_rect.center = position
        self.larger_border_rect.center = position
        self.text_rect.center = position

    def draw(self) -> None:
        """The draw method called to draw the button
        Draws the border, background and text in that order
        """
        super().draw()

        self.screen.fill(self.text_color, self.border_rect)
        if self.background_color != None:
            self.screen.fill(self.background_color, self.rect)
        self.screen.blit(self.text_rendered, self.text_rect)

    def handle_events(self, events: pygame.EventList):
        """Handles the events passed to this function, Usually by the screen.

        :param events: The events to be checked
        :type events: pygame.EventList
        """
        super().handle_events(events)

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.border_rect.collidepoint(event.pos):
                    self.border_rect = self.larger_border_rect
                    self.rect = self.larger_rect

                    self.text_rect = self.text_rendered.get_rect()
                    self.text_rect.center = self.border_rect.center
                else:
                    self.border_rect = self.normal_border_rect
                    self.rect = self.normal_rect

                    self.text_rect = self.text_rendered.get_rect()
                    self.text_rect.center = self.border_rect.center

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.callback_function is not None:
                    if self.border_rect.collidepoint(event.pos):
                        self.callback_function()
