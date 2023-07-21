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
from selenium.webdriver.common.action_chains import ActionChains

import winsound
import random

def namecheck(archive, nmin, fullname):

    splits = fullname.split()
    N = np.size(archive)
    flag = 0
    k_save = 0

    for i in splits:
        flag = 0
        if len(i) > nmin:
            for k in range(N):
                if flag == 0:
                    for j in archive[k]:
                        if j.lower() == i.lower():
                            flag = 1
                            k_save = k
                            break
                if flag == 1:
                    break
            if flag == 1:
                break

    return k_save, flag


def dozencheck(history):

    flag = 0

    for i in history:
        if i <= 12:
            flag = -1
            break

    if flag == 0:
        flag = 1

    if flag != 1:
        for i in history:
            if i <= 24 and i >= 13:
                flag = -2
                break

    if flag == -1:
        flag = 2

    if flag != 1 and flag != 2:
        for i in history:
            if i >= 25:
                flag = -3

    if flag == -2:
        flag = 3

    if flag == -1 or flag == -2 or flag == -3:
        flag = 0

    return flag


def rolls_add(flag, lobbyname):

    transfer_file = open(r"G:\Il mio Drive\Codes\Python\NoBet\Bot\rolls.dat", "r+")
    list = transfer_file.read()
    list_splits = list.split("\n")

    names = []

    for i in list_splits:
        if i != "":
            name = i.split("-")[0]
            name = name[:-1]            # I must remove the last space in name
            names.append(name)

    print(names)
    if not lobbyname in names:
        output = str(lobbyname) + " - " + str(flag) + "\n"
        transfer_file.write(output)

    transfer_file.close()


def rolls_remove(lobbyname):


    transfer_file = open(r"G:\Il mio Drive\Codes\Python\NoBet\Bot\rolls.dat", "r+")
    list = transfer_file.read()
    list_splits = list.split("\n")
    transfer_file.close()

    names = []
    dozens = []
    output = []

    for i in list_splits:
        if i != "":
            name = i.split("-")[0]
            dozen = i.split("-")[1]
            name = name[:-1]            # I must remove the last space in name
            names.append(name)
            dozens.append(dozen)

    for i in range(np.size(names)):
        if lobbyname != names[i]:
            single_out = str(names[i]) + " - " + str(dozens[i]) + "\n"
            output.append(single_out)
    
    transfer_file = open(r"G:\Il mio Drive\Codes\Python\NoBet\Bot\rolls.dat", "w")
    for j in output:
        transfer_file.write(j)

    transfer_file.close()


def strtoarr(array):

    for i in range(np.size(array)):
        array[i] = int(array[i])

    return array


def arrtostr(array):

    for i in range(len(array)):
        array[i] = str(array[i])

    return array


def multiple_inputs(current, history):
    
    flag = 0
    
    if np.array_equal(current, history):
        flag = 1

    return flag

def moneyring():
    winsound.PlaySound(r"G:\Il mio Drive\Codes\Python\NoBet\Archive\Data\Money.wav" , winsound.SND_ASYNC)


def scrollpage(driver):

    iteration = 1

    while iteration != 0:

        if iteration % 3 == 1:
            driver.execute_script("window.scrollTo(0, 1080)") 

        if iteration % 3 == 2:
            driver.execute_script("window.scrollTo(0, 2160)") 

        if iteration % 3 == 0:
            driver.execute_script("window.scrollTo(1080, 0)") 

        iteration = iteration + 1

        time.sleep(1)

    ### Scroll to a certain point
    # driver.execute_script("window.scrollTo(0, 1080)") 

    ### Scroll to the Bottom
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    ### Infinite Scroll -> Instagram
    # SCROLL_PAUSE_TIME = 0.5

    # # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")

    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     # Wait to load page
    #     time.sleep(SCROLL_PAUSE_TIME)

    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

def randomint(range):

    index = random.randint(0, range)

    return index



