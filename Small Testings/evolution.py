import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# importing sys
import sys
 
# adding Folder_2/subfolder to the system path
sys.path.insert(0, r'G:\Il mio Drive\Codes\Python\noBet\Bot')

import navigation as nav
import keys

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

driver = webdriver.Chrome(keys.chrome_path, options=keys.chrome_options)

driver, act, normalview, narrowview, wideview = nav.playtech_navigation_test(driver)

driver.switch_to.new_window('tab')
driver, act = nav.evolution_navigation(driver)

tables = nav.get_tables_evo(driver)

for table in tables:
    lobbyname = nav.get_lobbyname_evo(driver)
    print(lobbyname)

windows = driver.window_handles

