import time
import pika
import json
import threading
import urllib.parse as urlparse
from urllib.parse import parse_qs
import os
import sys

sys.path.append(os.getcwd())

from youtube_dl import YoutubeDL

if __name__ == '__main__':
    try:
        ydl = YoutubeDL()
        r = ydl.extract_info("https://www.youtuhbe.com/watch?v=Ths7YRthk4Q", False, "Youtube")
    except Exception as ex:
        print(ex.args)