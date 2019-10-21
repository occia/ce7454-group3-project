from bs4 import BeautifulSoup as bs
import urllib3
from PIL import Image
from io import BytesIO

# initialises pool manager for url requests
def init_url_manager():
    return urllib3.PoolManager()

# requests source code by url
def get_page(url_manager, url):
    return url_manager.request('GET', url)

# parses html code into readable format
def get_soup(res):
    return bs(res.data, 'html.parser')

# transforms image html into pillow image
def get_image(res):
    return Image.open(BytesIO(res.data))