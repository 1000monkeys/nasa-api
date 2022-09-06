import os
from pathlib import Path
from threading import Thread
import time
from urllib import request
from urllib.parse import urlparse

from helpers.image import Image


class Downloader(Thread):
    def __init__(self, screen, index, file_url, holder_dict, downloaders_list) -> None:
        super().__init__()
        self.screen = screen
        self.index = index
        self.file_url = file_url
        self.holder_dict = holder_dict
        self.downloaders_list = downloaders_list

        self.file_name = os.path.basename(urlparse(self.file_url).path)

    def run(self):
        if not Path("images\\" + self.file_name).is_file() and self.index not in self.downloaders_list:
            self.downloaders_list.append(self.index)
            
            request.urlretrieve(self.file_url, "images\\" + self.file_name)
            print("DLing: " + str(self.index) + " - " + self.file_name)

            time.sleep(0.25)

            print("Done DL: " + str(self.index) + " - " + self.file_name)
            self.downloaders_list.remove(self.index)

        image = Image(
            screen=self.screen,
            file_name=self.file_name
        )

        self.holder_dict[self.index] = image
