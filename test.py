import imagehash
import re
import telegram
import os
from urllib.request import urlopen
from PIL import Image

link = 'https://api.telegram.org/file/bot1087954382:AAHdqZOqFBOXGitrj64to9SzJxhxCEkeL2k/photos/file_1.jpg'
img = Image.open(os.path.abspath("imageHashBot/photo.jpg"))
print(imagehash.whash(img))
