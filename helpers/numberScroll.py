import pygame


class NumberScroll():
    def __init__(self, screen, indices, current_indice) -> None:
        self.screen = screen
        self.indices = indices
        self.current_indice = current_indice

        self.font_size = 24
        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)

        self.font = pygame.font.SysFont("arial", self.font_size)
        self.font_width, self.font_height = self.font.size(str(00))

        self.pointer = self.font.render(
            ">",
            True,
            self.text_color,
            self.background_color
        )

        self.text_rendereds = list()
        for index, indice in enumerate(self.indices):
            self.text_rendereds.append(self.font.render(
                str(indice),
                True,
                self.text_color,
                self.background_color
            ))

    def set_current_indice(self, current_indice):
        self.current_indice = current_indice

    def draw(self):
        self.screen.blit(self.pointer, (5, 115 + 9 * self.font_height + 9 * 5))
        for index, indice in enumerate(self.indices):
            self.screen.blit(self.text_rendereds[index], (20, 115 + ((index + 9) - self.current_indice) * self.font_height + ((index + 9) - self.current_indice) * 5))
