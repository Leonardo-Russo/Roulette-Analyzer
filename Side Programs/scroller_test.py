import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import keys
import library as lib
import markups as mu
import navigation as nav

import numpy as np
import time
import pandas as pd

from asyncore import read
from rich.traceback import install
install(show_locals = True)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains

# Error is "NoSuchElementException"

def scroller_test():

    driver = webdriver.Chrome(keys.chrome_path, options=keys.chrome_options)
    url = "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_iframe"
    driver.get(url)

    time.sleep(1)

    cookies = driver.find_element(by=By.ID, value="accept-choices")
    cookies.click()

    time.sleep(1)
    frame = driver.find_element(by=By.ID, value="iframeResult")
    driver.switch_to.frame(frame)

    time.sleep(1)
    frame = driver.find_element(by=By.XPATH, value="/html/body/iframe")
    driver.switch_to.frame(frame)

    time.sleep(1)
    cookies = driver.find_element(by=By.ID, value="accept-choices")
    cookies.click()

    driver.execute_script("window.scrollTo(0,300);")

    print("Press Enter to close the program...")
    input()
    driver.close()

scroller_test()