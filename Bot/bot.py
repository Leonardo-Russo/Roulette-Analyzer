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


### TO FIX ###
# There's an error with multiple inputs check when N_max is set to 10


bot = telebot.TeleBot(keys.API_KEY)
print("Bot has started...")

# Define Global Settings Variable
stoprolls = 0
settings = np.array([1, keys.N_max_display, keys.N_max_dzn, keys.N_max_colors, keys.n_afk, 0, keys.N_max_evorodd])        # [summary, max length, ...]
settings_name = ["Summary", "Display Size", "Dozen Check Size", "Color Check Size", "AAFK Interval", "AAFK Reports"]
sup = 0
pause = 0


@bot.message_handler(commands=['start'])
def start_command(message):
    user_name = message.from_user.first_name
    start_reply = f"Welcome {user_name} to the noBet Bot!\nType /help to show available commands."
    bot.send_message(message.chat.id, start_reply)


@bot.message_handler(commands=['bets'])
def bets_command(message):
    bets = open(r'C:\Users\Administrator\Desktop\Source\Archive\Data\bets_table.png', 'rb')
    bot.send_photo(message.chat.id, bets)
    bets.close()
    

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

    elif arg == "display":      # Allos to change Display Size
        try:
            arg2 = input[2]
            length_msg = "Maximum Display Size has been changed to: " + arg2
            settings[1] = int(arg2)
            bot.send_message(message.chat.id, length_msg)
        
        except:
            bot.send_message(message.chat.id, "Sorry, I couldn't change maximum display size :(")
            
    elif arg == "dozens":
        try:
            arg2 = input[2]
            length_msg = "Maximum Array Size for DozenCheck has been changed to: " + arg2
            settings[2] = int(arg2)
            bot.send_message(message.chat.id, length_msg)

        except:
            bot.send_message(message.chat.id, "Sorry, I couldn't change maximum array size :(")

    elif arg == "colors":
        try:
            arg2 = input[2]
            length_msg = "Maximum Array Size for ColorCheck has been changed to: " + arg2
            settings[3] = int(arg2)
            bot.send_message(message.chat.id, length_msg)

        except:
            bot.send_message(message.chat.id, "Sorry, I couldn't change maximum array size :(")
    
    elif arg == "aafk":
        try:
            arg2 = input[2]
            afk_msg = "AAFK Procedure will happen every " + arg2 + " iterations."
            settings[4] = int(arg2)
            bot.send_message(message.chat.id, afk_msg)

        except:
            bot.send_message(message.chat.id, "Sorry, I couldn't change the AAFK interval :(")

    elif arg == "aafk_report":          # Allows to watch AAFK procedure
        bot.send_message(message.chat.id, "Do you want to receive AAFK Report?", reply_markup=mu.aafk_report_markup())
        
    elif arg == "help":
        bot.send_message(message.chat.id, "/settings summary - to change summary preferences ...\n\n/settings display # - to change maximum display size to # ...\n\n/settings dozens # - to change DozenCheck size to # ...\n\n/settings colors # - to change ColorCheck size to # ...\n\n/settings aafk # - to change AAFK interval to # ...\n\n/settings aafk_rep - to change AAFK reports preferences.")
            

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

    if call.data == "aafk_rep_on":
        settings[5] = 1
        bot.answer_callback_query(call.id, "You have chosen to receive AAFK Reports.")
    elif call.data == "aafk_rep_off":
        settings[5] = 0
        bot.answer_callback_query(call.id, "You have chosen to NOT receive AAFK Reports.")


@bot.message_handler(commands=['rolls'])
def rolls_command(message):
    
    global stoprolls
    global settings
    global sup
    global pause

    bot.send_message(message.chat.id, 'Firing up the Engines!')

# try:

    ### PLANETWIN NAVIGATION ###
    driver = webdriver.Chrome(keys.chrome_path, options=keys.chrome_options)

    driver, act, summ_prep_msg, balance, normalview, narrowview, wideview = nav.playtech_navigation(driver, bot, message)
    wideview.click()

    driver.switch_to.new_window('tab')
    driver, act = nav.evolution_navigation(driver)

    playtech_window, evolution_window = driver.window_handles

    nav.switch_to_windowframe(driver, playtech_window, keys.playtech_frame)
    
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarting the iterations...")
    time.sleep(3)
    

    ### ROLLING ###
    iteration = 1
    lobbydata = []
    accepted_lobbies_index = []
    previous_afk_index = -1

    while stoprolls == 0:

        try:

            # Settings Update
            summary_switch = settings[0]
            max_display = settings[1]
            max_dozens = settings[2]
            max_colors = settings[3]
            n_aafk = settings[4]
            aafk_report = settings[5]
            max_evorodd = settings[6]

            # AAFK Reboot
            if iteration % keys.n_reboot == 0:
                reboot_msg = bot.send_message(message.chat.id, "Rebooting the Program...")
                driver, act, normalview, narrowview, wideview = nav.playtech_navigation_restart(driver, bot, message)
                bot.delete_message(message.chat.id, reboot_msg.message_id)
            
            # AAFK -> Enter and Exit Games to Avoid Inactivity
            if iteration % n_aafk == 0 and iteration % keys.n_reboot != 0:
                accepted_lobbies_index = []
                for t in range(np.size(tables)):
                    lobbyname = nav.get_lobbyname_play(tables[t])
                    if lobbyname in keys.accepted_lobbies_afk:
                        accepted_lobbies_index.append(t)        # indexes of all accepted lobbies

                if aafk_report:
                    aafk_report_msg = bot.send_message(message.chat.id, "Performing AAFK Procedure...")

                nav.aafk_exit(driver, act)

                if aafk_report:
                    bot.delete_message(message.chat.id, aafk_report_msg.message_id)

            # Pause Command
            if pause != 0:
                pause_msg = bot.send_message(message.chat.id, "Pausing Rolls...")
                time.sleep(pause)
                bot.delete_message(message.chat.id, pause_msg.message_id)
                pause = 0


            tables = nav.get_tables_play(driver)        # acquire all tables
            out = ""                                    # initialize output message

            for i in range(np.size(tables)):            # cycle through the tables

                table = tables[i]                       # analyse i-th Table

                lobbyname = nav.get_lobbyname_play(table)        # get lobbyname as text

                if lobbyname in keys.accepted_lobbies:      # checks if the lobby is acceptable

                    if lobbyname in keys.accepted_lobbies_toscroll:     # hover over table if necessary
                        act.move_to_element(table).perform()
                
                    lobbyhistory, valid_history = nav.get_lobbyhistory(table)       # get lobbyhistory as np.array and perform checks

                    if valid_history:       # only lobbyhistories that have passed the checks are analised

                        # 1st Iteration -> Create Database
                        if iteration == 1:

                            lobby = cls.lobby(lobbyname, lobbyhistory)  # define each element as a lobby element
                            lobbydata.append(lobby)                     # create initial database
                            out += lobby.summary(max_display) + '\n'    # build initial summary message                    

                        # Further Iterations -> Update Database
                        if iteration > 1:

                            for k in range(len(lobbydata)):

                                if lobbyname == lobbydata[k].name:

                                    if lib.different_arrays(lobbyhistory, lobbydata[k].history[0:10]):          # first looks for arrays that have changed, which means they have been updated
                                        addition_index = lib.joint_index(lobbyhistory, lobbydata[k].history[0:10])      # finds index of the first number in the new array such that after that point the arrays are equal
                                        lobbydata[k].update = 1         # flag the update in array
                                        if addition_index == 1:         # update the archive with new bits of array 
                                            lobbydata[k].history = np.hstack((lobbyhistory[0], lobbydata[k].history))
                                        if addition_index > 1:
                                            lobbydata[k].history = np.hstack((lobbyhistory[0:addition_index], lobbydata[k].history))
                                    else:
                                        lobbydata[k].update = 0         # if the arrays are detected they are flagged as non-updated

                                    if np.size(lobbydata[k].history) <= max_dozens:     # create proper sized arrays to use for the checks
                                        dozens_history = lobbydata[k].history

                                    if np.size(lobbydata[k].history) > max_dozens:
                                        dozens_history = lobbydata[k].history[0:max_dozens]

                                    if np.size(lobbydata[k].history) <= max_colors:
                                        colors_history = lobbydata[k].history

                                    if np.size(lobbydata[k].history) > max_colors:
                                        colors_history = lobbydata[k].history[0:max_colors]

                                    if np.size(lobbydata[k].history) <= max_evorodd:
                                        evorodd_history = lobbydata[k].history

                                    if np.size(lobbydata[k].history) > max_evorodd:
                                        evorodd_history = lobbydata[k].history[0:max_evorodd]

            
                                    # Create Summary Message
                                    out += lobbydata[k].summary(max_display) +'\n'

                                    # Check required Conditions
                                    flag_dozens = lib.dozencheck(dozens_history)
                                    flag_colors = lib.colorcheck(colors_history, lobbyname)
                                    flag_evorodd = lib.evenoroddcheck(evorodd_history)

                                    # Dozens Check
                                    if flag_dozens != 0 and lobbydata[k].update == 1:

                                        hooray_dzn = '*Hooray!* You should bet on Dozen n° ' + str(flag_dozens) + ' on ' + lobbyname
                                        bot.send_message(message.chat.id, hooray_dzn, parse_mode="Markdown")

                                        if lobbydata[k].after_dozens == 0:
                                            lobbydata[k].after_dozens = 1
                                        if lobbydata[k].after_dozens != 0:
                                            lobbydata[k].after_dozens += 1

                                    if flag_dozens == 0 and lobbydata[k].update == 1 and lobbydata[k].after_dozens != 0:

                                        attempt = lobbydata[k].after_dozens - 1
                                        attempts = "You would've won after " + str(attempt) + " attempts."
                                        bot.send_message(message.chat.id, attempts)
                                        print("You would've won after ", attempt, " attempts.")
                                        lobbydata[k].after_dozens = 0

                                    # Colors Check
                                    if flag_colors != 0 and lobbydata[k].update == 1:
                                        
                                        if flag_colors == 1:
                                            clr_bet = "Reds"
                                        if flag_colors == 2:
                                            clr_bet = "Blacks"

                                        hooray_clr = '*Hooray!* You should bet on ' + str(clr_bet) + ' on ' + lobbyname
                                        bot.send_message(message.chat.id, hooray_clr, parse_mode="Markdown")

                                        if lobbydata[k].after_colors == 0:
                                            lobbydata[k].after_colors = 1
                                        if lobbydata[k].after_colors != 0:
                                            lobbydata[k].after_colors += 1

                                    if flag_colors == 0 and lobbydata[k].update == 1 and lobbydata[k].after_colors != 0:

                                        attempt = lobbydata[k].after_colors - 1
                                        attempts = "You would've won after " + str(attempt) + " attempts."
                                        bot.send_message(message.chat.id, attempts)
                                        print("You would've won after ", attempt, " attempts.")
                                        lobbydata[k].after_colors = 0

                                    # Even/Odd Check
                                    if flag_evorodd != 0 and lobbydata[k].update == 1:
                                        
                                        if flag_evorodd == 1:
                                            evorodd_bet = "Even"
                                        if flag_evorodd == 2:
                                            evorodd_bet = "Odd"

                                        hooray_evorodd = '*Hooray!* You should bet on ' + str(evorodd_bet) + ' on ' + lobbyname
                                        bot.send_message(message.chat.id, hooray_evorodd, parse_mode="Markdown")

                                        if lobbydata[k].after_evorodd == 0:
                                            lobbydata[k].after_evorodd = 1
                                        if lobbydata[k].after_evorodd != 0:
                                            lobbydata[k].after_evorodd += 1

                                    if flag_evorodd == 0 and lobbydata[k].update == 1 and lobbydata[k].after_evorodd != 0:

                                        attempt = lobbydata[k].after_evorodd - 1
                                        attempts = "You would've won after " + str(attempt) + " attempts."
                                        bot.send_message(message.chat.id, attempts)
                                        print("You would've won after ", attempt, " attempts.")
                                        lobbydata[k].after_evorodd = 0


                                    break


            # Send Summary Message
            # print(out)        # sends message in console
            if summary_switch == 1:
                if iteration == 1:      # at the first iteration it creates the message
                    bot.delete_message(message.chat.id, summ_prep_msg.message_id)
                    time.sleep(0.5)
                    bot.send_message(message.chat.id, "*Summary Table:*", parse_mode="Markdown")
                    time.sleep(0.5)
                    summary_message = bot.send_message(message.chat.id, out)
                    out_old = out
                elif iteration > 1:     # for further iterations it updates the first message
                    if out != out_old:
                        bot.edit_message_text(out, message.chat.id, summary_message.message_id)
                        out_old = out
                        
            iteration = iteration + 1

            time.sleep(keys.iterations_dt)   # Interval Between Iterations

            # Sup Command
            if sup == 1:
                lib.sup_screenshot(message, bot)
                sup = 0

            # Quit Procedure
            if stoprolls == 1:
                driver.close()



        except:
            
            managed = nav.last_hope(driver, bot, message)
            if managed:
                time.sleep(2)
            else:
                bot.send_message(message.chat.id, "Aborting Rolling Process...")
                stoprolls = 1


# except:

    bot.send_message(message.chat.id, "Something went wrong... :(")
    lib.failure_screenshot(message, bot)
    time.sleep(2)
    driver.quit()


@bot.message_handler(commands=['stop'])
def stop_rolls_command(message):
    global stoprolls
    stoprolls = 1
    bot.send_message(message.chat.id, 'Quitting Rolling Process...')
    
    time.sleep(15)
    stoprolls = 0
    

@bot.message_handler(commands=['sup'])
def sup_bro(message):
    global sup
    sup = 1


@bot.message_handler(commands=['pause'])
def pause_rolls(message):

    input = message.text.lower().split(" ")
    
    if np.size(input) > 1:
        arg = input[1]
    else:
        arg = ""

    global pause

    try:
        pause = int(arg)
    except:
        bot.send_message(message.chat.id, "Error! Please specify valid value of Wait Time.")
    


bot.infinity_polling()