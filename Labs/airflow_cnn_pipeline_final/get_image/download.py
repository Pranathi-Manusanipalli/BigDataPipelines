import urllib.request
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def fetch(img_url):
    urllib.request.urlretrieve(img_url, os.path.basename(img_url))

    return os.path.basename(img_url)





