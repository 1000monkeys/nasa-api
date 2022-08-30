import os
from pathlib import Path
from threading import Thread
import time
from urllib import request
from urllib.parse import urlparse


class Downloader(Thread):
    def __init__(self, index, file_url, callback) -> None:
        super().__init__()
        self.file_url = file_url

        self.file_name = os.path.basename(urlparse(self.file_url).path)
       
        self.index = index
        self.callback = callback

    def run(self):
        if not Path("images/" + self.file_name).is_file():
            request.urlretrieve(self.file_url, "images/" + self.file_name)
            print("DLing: " + self.file_name)

            self.callback(self.index, self.file_name)
            print("Done DL!")
