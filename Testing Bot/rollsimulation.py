from cgi import print_form
from dataclasses import dataclass
import telebot
import keys as keys
import library as lib
import numpy as np
import classes as cls

import time
import pandas as pd

from asyncore import read
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import re

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import markups as mu

import library as lib


def fakerolls():

    data = []
    stoprolls = 0
    N_max = 15
    time_interval = 0.001
    n_lobbies = 15
    asktime = 100
    waittime = 1

    attempts = []
    attempts_file = open(r"G:\Il mio Drive\Codes\Python\noBet\Testing Bot\attempts.txt", "a+")
    # Note that I can also append things to split the process in multiple ones

    print("Press Enter to simulate the rolling...")
    input()

    out = ""

    # Build Initial Array
    lobbynames = ["Lob1", "Lob2", "Lob3", "Lob4", "Lob5", "Lob6", "Lob7", "Lob8", "Lob9", "Lob10", "Lob11", "Lob12", "Lob13", "Lob14", "Lob15",]
    for i in range(n_lobbies):

        lobbyhistory = np.random.randint(37, size=10)
        lobbyname = lobbynames[i]

        # Build the lobby
        lobby = cls.lobby(lobbyname, lobbyhistory)

        # Append the lobby to the array
        data.append(lobby)

        out += lobby.summary(N_max) +'\n'

    print(out)


    iteration = 1
    # Simulate Iterative Process
    while stoprolls == 0:

        out = ""
        
        for i in range(len(data)):
            
            lobbyname = data[i].name
            lobbyhistory = data[i].history[0:10]

            newornot = int(np.random.randint(2, size=1))
            if newornot:
                new = np.random.randint(37, size=1)
                lobbyhistory = np.hstack((new, lobbyhistory[0:9]))

            if not np.array_equal(data[i].history[0:10], lobbyhistory):
                data[i].history = np.hstack((new, data[i].history))
                data[i].update = 1
            
            if np.size(data[i].history) <= (N_max-1):
                lobbyhistory = data[i].history
            else:
                lobbyhistory = data[i].history[0:N_max]

            out += data[i].summary(N_max) + '\n'

            # Check for Conditions -> DozenCheck
            flag = lib.dozencheck(lobbyhistory)

            if flag != 0 and data[i].update == 1:
                print(' ', '-'*100, '\nHOORAY! You should bet on Dozen n° ', flag, ' on ', lobbyname, '\n', '-'*100)         # Console Hooray
                data[i].update = 0

                if data[i].after == 0:
                    data[i].after = 1
                if data[i].after != 0:
                    data[i].after += 1

                lib.moneyring()
                time.sleep(waittime)

            if flag == 0 and data[i].update == 1 and data[i].after != 0:
                attempt = data[i].after - 1
                print("You would've won after ", attempt, " attempts.")
                attempts.append(attempt)
                toappend = str(attempt) + '\n'
                attempts_file.write(toappend)
                # print("\nPlease, press enter to continue...")
                # input()
                data[i].after = 0
                time.sleep(waittime)

        print(out)


        if iteration % asktime == 0:
            print("Do you want to continue?\n1. Yes\n2. No")
            answ = int(input())
            if answ == 2:
                stoprolls = 1
                attempts_file.close()

        iteration = iteration + 1
            
        time.sleep(time_interval)


fakerolls()