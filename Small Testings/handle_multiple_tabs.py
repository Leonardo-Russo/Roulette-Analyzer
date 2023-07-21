import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import numpy as np
import time
import pandas as pd

from asyncore import read
from rich.traceback import install
install(show_locals = True)

import pyautogui

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.options import Options as ChromeOptions

url = "https://www.google.it/"

chrome_path = "C:\Program Files (x86)\chromedriver.exe"

chrome_options = ChromeOptions()
chrome_options.add_argument("disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_path, options=chrome_options)
driver.get(url)
old_window = driver.current_window_handle

for i in range(5):

    time.sleep(2)
    if i % 2 == 0:
        driver.execute_script("window.open('about:blank', 'eventab');")
        driver.switch_to.window("eventab")
    else:
        driver.execute_script("window.open('about:blank', 'oddtab');")
        driver.switch_to.window("oddtab")
    windows = driver.window_handles
    print(windows)
    driver.get(url)
    driver.switch_to.window(windows[0])
    driver.close()
    # driver.switch_to(windows[1])



    