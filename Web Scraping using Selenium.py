#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# https://www.analyticsvidhya.com/blog/2020/08/web-scraping-selenium-with-python/
# https://towardsdatascience.com/web-scraping-e-commerce-website-using-selenium-1088131c8541
import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


# In[ ]:


os.chdir('/home/senzmatepc3/Desktop/img2/')
baseDir=os.getcwd()


# In[ ]:


#Headless chrome browser
from selenium import webdriver 
opts = webdriver.ChromeOptions()
opts.headless =True
driver =webdriver.Chrome(ChromeDriverManager().install(),options=opts)
count = 0
link_count = 63
while (link_count < 100):
    search_url="https://www.autobidmaster.com/en/carfinder-online-auto-auctions/?damage=MINOR%20DENT%2FSCRATCHES&sort=current_bid&order=desc&page={}".format(link_count) 
    driver.get(search_url)

    #Scroll to the end of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)#sleep_between_interactions

    links=[]
    for dr in driver.find_elements_by_tag_name('td'):
        for a in dr.find_elements_by_tag_name('div'):
            for q in a.find_elements_by_tag_name('a'):
                link = q.get_attribute('href')
                links.append(link)
    print(len(links))
    _links = np.unique(links).tolist()

    for link in _links:
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)#sleep_between_interactions
        img=[]
        for tag in driver.find_elements_by_tag_name('img'):
            img_link = tag.get_attribute('src')
            img.append(img_link)
        img = list(filter(None, img))
        _img = np.unique(img).tolist()
        _img = list(filter(lambda k: '.svg' not in k, _img))
        print(len(_img),_img)
        
        for url in _img:
            file_name = "{}_{}.jpg".format(link_count,count)   
            try:
                image_content = requests.get(url).content

            except Exception as e:
                print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")

            try:
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')

                file_path = os.path.join(baseDir, file_name)

                with open(file_path, 'wb') as f:
                    image.save(f, "JPEG", quality=100)
                print(f"SAVED - {url} - AT: {file_path}")
            except Exception as e:
                print(f"ERROR - COULD NOT SAVE {url} - {e}")
            count+=1   
    link_count+=1        

