import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import keys
import library as lib
import markups as mu
import navigation as nav
import classes as cls

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

### Description ###
# ...

### TO FIX ###
# There's a problem with the AAFK procedure. Temporarly fixed.
#
# I need to find the XPATH of the confirmation code button and click it through that instead of class.
#
# I need to figure out a way to wait for the bid to be placeable -> read the clock!
#
# Make AUTOPILOT toggleable

### IMPROVEMENTS ###
# The way the program works now is that it acquire an array with all the tables under the i-th index. Then it takes each one and
# tries to find another with the same name (meaning it has found itself) in the database.
# The thing is that it has to cycle at first through all the tables under the i index, and then it has to match the name of that
# table with one in the database, then it updates the database.
#
# Wouldn't it be a lot faster if e only used one index? Is it possible?

bot = telebot.TeleBot(keys.API_KEY)
print("Bot has started...")

# Define Global Settings Variable
stoprolls = 0
settings = np.array([0, keys.N_storage, keys.n_afk, 0])        # [summary, max length, ...]
settings_name = ["Summary", "Maximum Size", "AAFK Interval", "AutoPilot (Experimental)"]


@bot.message_handler(commands=['start'])
def start_command(message):
    user_name = message.from_user.first_name
    start_reply = f"Welcome {user_name} to the noBet Bot!\nType /help to show available commands."
    bot.send_message(message.chat.id, start_reply)
    

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Here's the list of available commands:\n/rolls - to start printing matches.\n/stop - to stop rolling process.\n/settings - to change preferences.")


@bot.message_handler(commands=['settings'])
def message_handler(message):

    input = message.text.lower().split(" ")
    
    if np.size(input) > 1:
        arg = input[1]
    else:
        arg = ""

    global settings

    if arg == "":           # Builds a list of current Settings
        settings_out = ""
        for i in range(np.size(settings)):
            if settings[i] == 1:
                flag = "On"
            elif settings[i] == 0:
                flag = "Off"
            else:
                flag = str(settings[i])

            settings_out = settings_out + settings_name[i] + " is set to: " + flag + "\n"
        settings_out = settings_out + "\nTo change each parameter you may type:\n/settings help"
        bot.send_message(message.chat.id, settings_out)

    elif arg == "summary":      # Allows to change Summary Settings
        bot.send_message(message.chat.id, "Do you want to receive Summaries?", reply_markup=mu.summ_markup())

    elif arg == "length":
        try:
            arg2 = input[2]
            length_msg = "Maximum Array Size has been changed to: " + arg2
            settings[1] = int(arg2)
            bot.send_message(message.chat.id, length_msg)

        except:
            bot.send_message(message.chat.id, "Sorry, I couldn't change maximum array size :(")
    
    elif arg == "afk":
        try:
            arg2 = input[2]
            afk_msg = "AAFK Procedure will happen every " + arg2 + " iterations."
            settings[2] = int(arg2)
            bot.send_message(message.chat.id, afk_msg)

        except:
            bot.send_message(message.chat.id, "Sorry, I couldn't change the AAFK interval :(")

    elif arg == "help":
        bot.send_message(message.chat.id, "/settings summary - to change summary preferences\n\n/settings length # - to change maximum array size to #\n\n/settings afk # - to change AAFK interval to #.")
            

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Recall Global Variable
    global settings

    if call.data == "summ_on":
        settings[0] = 1
        bot.answer_callback_query(call.id, "You have chosen to receive Summary Messages.")
    elif call.data == "summ_off":
        settings[0] = 0
        bot.answer_callback_query(call.id, "You have chosen to NOT receive Summary Messages.")


@bot.message_handler(commands=['rolls'])
def rolls_command(message):
    
    global stoprolls
    global settings

    bot.send_message(message.chat.id, 'Firing up the Engines!')

    try:

        ### PLANETWIN NAVIGATION ###

        driver = webdriver.Chrome(keys.chrome_path, options=keys.chrome_options)
        # driver = webdriver.Firefox(executable_path = keys.firefox_path, options=keys.firefox_options)
        driver.get(keys.url)

        # Login #
        nav.login(driver)

        # Roulette SubSection Click #
        time.sleep(2)       # loading time...
        nav.roulette(driver)

        # Roulette Italiana Click #
        time.sleep(1)
        act = ActionChains(driver)
        nav.thumbnails(driver, act)

        # Exit to Summary Screen -> Switch to iframe with ID = gameFrame #
        time.sleep(1)
        nav.gameframe(driver)

        bot.send_message(message.chat.id, "...almost there...")

        # Close Button #
        time.sleep(1)


        ### AUTOPILOT TEST ###
        nav.enter_amount(driver, balance="5")
        nav.confirm_amount(driver)
        nav.confirmation_code(driver)

        # Acquire Chips
        chips, chip_05, chip_1, chip_5, chip_10, chip_25 = nav.get_chips(driver)
        chip_05.click()

        # Acquire Dozens
        first_dozen, second_dozen, third_dozen = nav.get_dozens(driver)

        # se è presente il countdown non posso giocare!


        ### Try to Read Timer ###
        print("Press Enter to look for Timer...")
        input()
        nav.get_timer(driver)
        
        ################ Test Bid ################
        print("Press Enter to bid...")
        input()

        bid_counter = 0
        if nav.bid_dozen(driver, first_dozen, chip_05):
            bid_counter += 1
        else:
            bot.send_message(message.chat.id, "There was an error in the bidding process!")
        
        print("The next bid should be: " + str(0.5*2**bid_counter))

        time.sleep(120)
        ###

        nav.closebutton(driver)
        time.sleep(1)
        balance = nav.get_balance(driver, bot, message)

        # Change Slide to Roulette #
        time.sleep(2)
        nav.playtech_roulette(driver)

        # Acquire Views #
        time.sleep(2)
        wideview, normalview, narrowview = nav.acquire_views(driver)
        normalview.click()
        narrowview.click()
        wideview.click()
        
        print("Starting the iterations...")
        time.sleep(5)

        
        ### ROLLING ###

        iteration = 1
        lobbydata = []
        accepted_lobbies_index = []

        while stoprolls == 0:

            tables = nav.get_tables(driver, act)        # acquire all tables
            out = ""                                    # initialize output message

            # Settings Update
            summary_switch = settings[0]
            max_length = settings[1]
            n_aafk = settings[2]

            # AAFK -> Enter and Exit Games to Avoid Inactivity
            if iteration % n_aafk == 0:
                afk_index = lib.randomint(np.size(accepted_lobbies_index)-1)
                # nav.aafk(driver, tables[accepted_lobbies_index[afk_index]])       # to be reintroduced!
                nav.aafk_prov(driver, tables[2], tables[6])     # force the choice between Roulette Italiana and American Roulette only
                tables = nav.get_tables(driver, act)

            for i in range(np.size(tables)):            # cycle through the tables

                table = tables[i]                       # analyse i-th Table

                # Get Lobbyname as text
                lobbyname = nav.get_lobbyname(table)

                if lobbyname in keys.accepted_lobbies:
                    
                    act.move_to_element(table).perform()        # hover over table
                    
                    # Get Lobbyhistory as np.array and Perform Checks
                    lobbyhistory, valid_history = nav.get_lobbyhistory(table)

                    if valid_history:

                        # 1st Iteration -> Create Database
                        if iteration == 1:

                            lobby = cls.lobby(lobbyname, lobbyhistory)
                            lobbydata.append(lobby)
                            accepted_lobbies_index.append(i)            # indexes of all accepted lobbies       
                            out += lobby.summary(max_length) +'\n'      # build initial summary message                    

                        # Further Iterations -> Update Database
                        if iteration > 1:

                            for k in range(len(lobbydata)):

                                if lobbyname == lobbydata[k].name:

                                    if not np.array_equal(lobbyhistory, lobbydata[k].history[0:10]):
                                        lobbydata[k].history = np.hstack((lobbyhistory[0], lobbydata[k].history))
                                        lobbydata[k].update = 1

                                    if np.size(lobbydata[k].history) <= max_length:
                                        lobbyhistory = lobbydata[k].history

                                    if np.size(lobbydata[k].history) > max_length:
                                        lobbyhistory = lobbydata[k].history[0:max_length]

                                    # Multiple Inputs check
                                    if lib.multiple_inputs(lobbyhistory, lobbydata[k].history[0:10]) and np.size(lobbydata[k].history) > 10:
                                        multiple_inputs_text = "Multiple Inputs detected from " + lobbyname
                                        bot.send_message(message.chat.id, multiple_inputs_text)

                                    # Create Summary Message
                                    out += lobbydata[k].summary(max_length) +'\n'

                                    # Check for Conditions -> DozenCheck
                                    flag = lib.dozencheck(lobbyhistory)

                                    if flag != 0 and lobbydata[k].update == 1:

                                        hooray = 'Hooray! You should bet on Dozen n° ' + str(flag) + ' on ' + lobbyname
                                        bot.send_message(message.chat.id, hooray)
                                        print(' ', '-'*100, '\nHOORAY! You should bet on Dozen n° ', flag, ' on ', lobbyname, '\n', '-'*100)         # Console Hooray

                                        ####### INTRODUCE AutoPilot #######
                                        bot.send_message(message.chat.id, "Starting AutoPilot")
                                        tables[i].click()

                                        balance = nav.get_balance(driver, bot, message)

                                        nav.enter_amount(driver, balance)

                                        print("Press Enter to continue...")
                                        input()

                                        lobbydata[k].update = 0

                                        if lobbydata[k].after == 0:
                                            lobbydata[k].after = 1
                                        if lobbydata[k].after != 0:
                                            lobbydata[k].after += 1

                                    if flag == 0 and lobbydata[k].update == 1 and lobbydata[k].after != 0:

                                        attempt = lobbydata[k].after - 1
                                        attempts = "You would've won after " + str(attempt) + " attempts."
                                        bot.send_message(message.chat.id, attempts)
                                        print("You would've won after ", attempt, " attempts.")
                                        lobbydata[k].after = 0


                                    break


            # Send Summary Message
            if iteration >= 1:
                print(out)
                if summary_switch == 1:
                    bot.send_message(message.chat.id, out)
                        
            iteration = iteration + 1

            time.sleep(keys.iterations_dt)   # Interval Between Iterations

            # Quit Procedure
            if stoprolls == 1:
                driver.quit()

    except:
        bot.send_message(message.chat.id, "Something went wrong... :(")
        time.sleep(5)
        driver.close()


@bot.message_handler(commands=['stop'])
def stop_rolls_command(message):
    global stoprolls
    stoprolls = 1
    bot.send_message(message.chat.id, 'Quitting Rolling Process...')
    
    time.sleep(15)
    stoprolls = 0

@bot.message_handler(commands=['test'])
def test_function(message):

    failure_screen = pyautogui.screenshot()
    failure_screen.save(r'C:\Users\Administrator\Desktop\Source\Screenshots\failure_screenshot.png')
    time.sleep(3)
    failure_screenshot = open(r'C:\Users\Administrator\Desktop\Source\Screenshots\failure_screenshot.png', 'rb')
    bot.send_photo(message.chat.id, failure_screenshot)
    failure_screenshot.close()
    

@bot.message_handler(commands=['sup'])
def sup_bro(message):
    
    sup_screen = pyautogui.screenshot()
    sup_screen.save(r'C:\Users\Administrator\Desktop\Source\Screenshots\sup_screenshot.png')
    time.sleep(1)
    sup_screen = open(r'C:\Users\Administrator\Desktop\Source\Screenshots\sup_screenshot.png', 'rb')
    bot.send_photo(message.chat.id, sup_screen)
    sup_screen.close()


bot.infinity_polling()