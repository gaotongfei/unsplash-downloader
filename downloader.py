import requests
import uuid
import shutil
import re
import logging
from bs4 import BeautifulSoup
import os
import time
from multiprocessing.dummy import Pool as ThreadPool

logging.basicConfig(level=logging.ERROR, filename='error.log')
requests.packages.urllib3.disable_warnings()

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures')
if not os.path.exists(path):
    os.makedirs(path)


def get_url(url):
    try:
        print('scraping ' + url)
        r = requests.get(url, verify=False, timeout=30)
        make_soup(r)
        time.sleep(10)
    except Exception:
        logging.exception("error")

def downloader(url):
    try:
        time.sleep(10)
        r = requests.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            print("status code 200")
            with open(os.path.join(path, str(uuid.uuid4()) + '.jpg'), 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except Exception:
        print("status code not 200")
        logging.exception("error")

def make_soup(response):
    soup = BeautifulSoup(response.text, "html.parser")
    url = [x['src'] for x in soup.select('img.photo__image.js-fluid-image.js-grid-image')]
    img_urls.extend(url)

if __name__ == '__main__':
    PAGE = 3
    urls = ['https://unsplash.com/?page={}'.format(page) for page in range(PAGE)]
    img_urls = []
    pool = ThreadPool(14)
    pool.map(get_url, urls)
    print(img_urls)
    pool.map(downloader, img_urls)
    pool.close()
    pool.join()
