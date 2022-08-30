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

        self.sol = 0

        self.API_KEY = "J3gNT5GSEJBFVCanDTzj9aDUMdBuMDd94SGNPXcz"

        pygame.init()

        self.rect = (1024, 786)

        self.screen = pygame.display.set_mode(self.rect)
        pygame.display.set_caption("NASA Images")

    def get_rect(self):
        return self.rect

    def previous_image(self):
        self.image_pos = self.image_pos - 1
        
        if self.image_pos < 0:
            self.image_pos = 0

        self.number_scroll.set_current_indice(self.image_pos)

    def next_image(self):
        self.download_next_images()

        self.image_pos = self.image_pos + 1

        if self.image_pos not in self.indices:
            self.image_pos = self.image_pos - 1

        self.number_scroll.set_current_indice(self.image_pos)
        #print(self.image_pos)

    def set_sol(self):
        self.sol = self.text_input_sol.get_input()
        self.get_sol_data()
        self.image_pos = 0
        self.number_scroll = NumberScroll(
            self.screen,
            self.indices,
            current_indice=0
        )

    def get_sol_data(self):
        url = "https://api.nasa.gov/mars-photos/api/v1/rovers/" + self.rover + "/photos?sol=" + str(self.sol) + "&api_key=" + self.API_KEY

        #print(url)

        r = requests.get(url)
        self.data = r.json()

        self.indices = list()
        for index, photo in enumerate(self.data["photos"]):
            self.indices.append(index)
        
        self.number_scroll = NumberScroll(
            self.screen,
            self.indices,
            current_indice=0
        )

        self.download_next_images()

    def download_next_images(self):
        count = self.image_pos
        if (count + 4) in self.indices:
            for photo in self.data["photos"][count:count+5]:
                #print(count)
                if count not in self.images.keys():
                    file_name = os.path.basename(urlparse(photo['img_src']).path)
                    if not Path("images/" + file_name).is_file():
                        download = Downloader(count, photo['img_src'], self.add_downloaded_image)
                        download.start()
                    else:
                        self.add_downloaded_image(count, file_name)
                count = count + 1

    def add_downloaded_image(self, index, file_name):
        self.images[index] = Image(
            screen=self.screen,
            file_name=file_name
        )

    def check_exist(self, file_name):
        if Path("images/" + self.file_name).is_file():
            return True
        else:
            return False

    def set_curiosity(self):
        self.rover = "curiosity"
        self.URL = self.CUR_URL

        self.curiosity.background_color = (0, 255, 0)
        self.opportunity.background_color = (255, 255, 255)
        self.spirit.background_color = (255, 255, 255)

        self.images = dict()
        self.set_rover()

    def set_opportunity(self):
        self.rover = "opportunity"
        self.URL = self.OPP_URL

        self.curiosity.background_color = (255, 255, 255)
        self.opportunity.background_color = (0, 255, 0)
        self.spirit.background_color = (255, 255, 255)

        self.images = dict()
        self.set_rover()

    def set_spirit(self):
        self.rover = "spirit"
        self.URL = self.SPU_URL

        self.curiosity.background_color = (255, 255, 255)
        self.opportunity.background_color = (255, 255, 255)
        self.spirit.background_color = (0, 255, 0)

        self.images = dict()
        self.set_rover()
    
    def set_rover(self):
        r = requests.get(self.URL)
        data = r.json()

        #print(data)

        self.sols = list()
        for photo_data in data["photo_manifest"]["photos"]:
            self.sols.append(photo_data["sol"])

        max_sol = data["photo_manifest"]["max_sol"]
        print(max_sol)
        self.sol = max_sol
        self.text_input_sol.set_input(str(self.sol))
        self.get_sol_data()

    def run(self):
        self.CUR_URL = "https://api.nasa.gov/mars-photos/api/v1/manifests/Curiosity?api_key=" + self.API_KEY
        self.OPP_URL = "https://api.nasa.gov/mars-photos/api/v1/manifests/Opportunity?api_key=" + self.API_KEY
        self.SPU_URL = "https://api.nasa.gov/mars-photos/api/v1/manifests/Spirit?api_key=" + self.API_KEY
        self.URL = self.CUR_URL

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
        self.text_input_sol.set_input(str(self.sol))
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

        self.set_curiosity()
        self.set_rover()

        while True:
            pygame.time.Clock().tick(30)
            events = pygame.event.get()

            self.handle_events(events)

            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.rect[0], self.rect[1]))

            if self.image_pos in self.indices:
                if self.image_pos in self.images.keys():
                    self.images[self.image_pos].handle_events(events)
                    self.images[self.image_pos].draw()

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
