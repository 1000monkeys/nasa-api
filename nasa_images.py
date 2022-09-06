from cgitb import text
import os
from pathlib import Path
from turtle import right
from urllib.parse import urlparse
import requests
import pygame
from helpers.downloader import Downloader
from helpers.numberScroll import NumberScroll
from helpers.textInput import TextInput
from helpers.button import Button
from helpers.screen import Screen
from helpers.image import Image


class NASAImages(Screen):
    def __init__(self):
        self.image_pos = 0

        self.images = dict()
        self.images["curiosity"] = dict()
        self.images["opportunity"] = dict()
        self.images["spirit"] = dict()

        self.downloaders = list()

        self.data = dict()
        self.data["curiosity"] = dict()
        self.data["opportunity"] = dict()
        self.data["spirit"] = dict()

        self.API_KEY = "J3gNT5GSEJBFVCanDTzj9aDUMdBuMDd94SGNPXcz"

        pygame.init()

        self.rect = (1024, 786)

        self.screen = pygame.display.set_mode(self.rect)
        pygame.display.set_caption("NASA Images")

        self.left_button = Button(
            screen=self.screen,
            text="<",
            position=(110, 25),
            text_color=(0, 0, 0),
            background_color=(255, 255, 255),
            border_color=(128, 128, 128),
            border_size=2, 
            font_size=48,
            padding=5,
            callback_function=self.previous_image
        )
        self.right_button = Button(
            screen=self.screen,
            text=">",
            position=(160, 25),
            text_color=(0, 0, 0),
            background_color=(255, 255, 255),
            border_color=(128, 128, 128),
            border_size=2, 
            font_size=48,
            padding=5,
            callback_function=self.next_image
        )

        self.text_input_sol = TextInput(
            screen=self.screen,
            text="0",
            position=(300, 25),
            text_color=(0, 0, 0),
            background_color=(128, 128, 128),
            border_color=(255, 255, 255),
            border_width=2,
            max=4
        )
        self.submit_button = Button(
            screen=self.screen,
            text="Set Sol",
            position=(430, 32),
            text_color=(0, 0, 0),
            background_color=(255, 255, 255),
            border_color=(128, 128, 128),
            border_size=2, 
            font_size=24,
            padding=5,
            callback_function=self.set_sol
        )

        self.curiosity = Button(
            screen=self.screen,
            text="Curiosity",
            position=(525, 32),
            text_color=(0, 0, 0),
            background_color=(255, 255, 255),
            border_color=(128, 128, 128),
            border_size=2, 
            font_size=24,
            padding=5,
            callback_function=self.set_curiosity
        )

        self.opportunity = Button(
            screen=self.screen,
            text="Opportunity",
            position=(625, 32),
            text_color=(0, 0, 0),
            background_color=(255, 255, 255),
            border_color=(128, 128, 128),
            border_size=2, 
            font_size=24,
            padding=5,
            callback_function=self.set_opportunity
        )

        self.spirit = Button(
            screen=self.screen,
            text="Spirit",
            position=(750, 32),
            text_color=(0, 0, 0),
            background_color=(255, 255, 255),
            border_color=(128, 128, 128),
            border_size=2, 
            font_size=24,
            padding=5,
            callback_function=self.set_spirit
        )

        self.CUR_URL = "https://api.nasa.gov/mars-photos/api/v1/manifests/Curiosity?api_key=" + self.API_KEY
        self.OPP_URL = "https://api.nasa.gov/mars-photos/api/v1/manifests/Opportunity?api_key=" + self.API_KEY
        self.SPU_URL = "https://api.nasa.gov/mars-photos/api/v1/manifests/Spirit?api_key=" + self.API_KEY

        self.URL = self.CUR_URL
        self.set_curiosity()

    def get_rect(self):
        return self.rect

    def previous_image(self):
        self.image_pos = self.image_pos - 1
        
        if self.image_pos < 0:
            self.image_pos = 0

        self.number_scroll.set_current_indice(self.image_pos)

    def next_image(self):
        self.image_pos = self.image_pos + 1

        if self.image_pos not in self.indices:
            self.image_pos = self.image_pos - 1

        self.number_scroll.set_current_indice(self.image_pos)
        #print(self.image_pos)

    def set_sol(self):
        self.sol = self.text_input_sol.get_input()
        self.image_pos = 0
        self.get_sol_data()
        self.number_scroll = NumberScroll(
            self.screen,
            self.indices,
            current_indice=0
        )

    def set_rover(self):
        r = requests.get(self.URL)

        print(self.URL)

        temp = r.json()

        self.sols = list()
        for photo in temp["photo_manifest"]["photos"]:
            self.sols.append(photo["sol"])

        max_sol = temp["photo_manifest"]["max_sol"]
        #print(max_sol)
        self.sol = max_sol
        self.text_input_sol.set_input(str(self.sol))
        self.get_sol_data()

    def get_sol_data(self):
        url = "https://api.nasa.gov/mars-photos/api/v1/rovers/" + self.rover + "/photos?sol=" + str(self.sol) + "&api_key=" + self.API_KEY

        print(url)

        r = requests.get(url)
        self.data[self.rover][self.sol] = r.json()

        self.indices = list()
        for index, photo in enumerate(self.data[self.rover][self.sol]["photos"]):
            self.indices.append(index)
        
        self.number_scroll = NumberScroll(
            self.screen,
            self.indices,
            current_indice=0
        )

    """
    def download_next_images(self):
        count = self.image_pos
        if (count + 4) in self.indices:
            for photo in self.data[self.rover][self.sol]["photos"][count:count+5]:
                #print(count)
                if self.sol not in self.images[self.rover].keys():
                    self.get_sol_data()
                
                if self.sol not in self.images[self.rover].keys():
                    self.images[self.rover][self.sol] = dict()
                
                if count not in self.images[self.rover][self.sol].keys() and count not in self.downloaders:
                    file_name = os.path.basename(urlparse(photo['img_src']).path)
                    download = Downloader(self.screen, count, photo['img_src'], self.images[self.rover][self.sol], self.downloaders)
                    self.downloaders.append(count)
                    download.start()
                count = count + 1
    """

    def check_exist(self, file_name):
        if Path("images\\" + file_name).is_file():
            return True
        else:
            return False

    def set_curiosity(self):
        self.rover = "curiosity"
        self.URL = self.CUR_URL

        self.curiosity.background_color = (0, 255, 0)
        self.opportunity.background_color = (255, 255, 255)
        self.spirit.background_color = (255, 255, 255)

        self.set_rover()

    def set_opportunity(self):
        self.rover = "opportunity"
        self.URL = self.OPP_URL

        self.curiosity.background_color = (255, 255, 255)
        self.opportunity.background_color = (0, 255, 0)
        self.spirit.background_color = (255, 255, 255)

        self.set_rover()

    def set_spirit(self):
        self.rover = "spirit"
        self.URL = self.SPU_URL

        self.curiosity.background_color = (255, 255, 255)
        self.opportunity.background_color = (255, 255, 255)
        self.spirit.background_color = (0, 255, 0)

        self.set_rover()

    def run(self):
        while True:
            pygame.time.Clock().tick(30)
            events = pygame.event.get()

            self.handle_events(events)

            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.rect[0], self.rect[1]))


            self.left_button.handle_events(events)
            self.left_button.draw()

            self.right_button.handle_events(events)
            self.right_button.draw()

            self.text_input_sol.handle_events(events)

            if len(self.text_input_sol.text) > 0 and int(self.text_input_sol.text) in self.sols:
                self.text_input_sol.background_color = (0, 255, 0)
            else:
                self.text_input_sol.background_color = (255, 0, 0)
            self.text_input_sol.draw()

            self.submit_button.handle_events(events)
            self.submit_button.draw()

            self.number_scroll.draw()

            self.curiosity.draw()
            self.curiosity.handle_events(events)

            self.opportunity.draw()            
            self.opportunity.handle_events(events)

            self.spirit.draw()
            self.spirit.handle_events(events)

            if self.sol not in self.images[self.rover].keys():
                self.images[self.rover][self.sol] = dict()

            if self.image_pos not in self.downloaders and self.image_pos not in self.images[self.rover][self.sol].keys():
                download = Downloader(self.screen, self.image_pos, self.data[self.rover][self.sol]["photos"][self.image_pos]['img_src'], self.images[self.rover][self.sol], self.downloaders)
                download.start()

            if self.image_pos in self.images[self.rover][self.sol].keys() and  isinstance(self.images[self.rover][self.sol][self.image_pos], Image):
                self.images[self.rover][self.sol][self.image_pos].handle_events(events)
                self.images[self.rover][self.sol][self.image_pos].draw()

            pygame.display.flip()


nasaImages = NASAImages()
nasaImages.run()

"""
r = requests.get(OPP_URL)
data = r.json()
print(data)

r = requests.get(SPU_URL)
data = r.json()
print(data)
"""
