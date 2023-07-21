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


def login(driver):

    while True:
        try:
            login = driver.find_elements(by=By.CLASS_NAME, value = "top-menu-input-w.input-text.w126")
            button = driver.find_element(by=By.CLASS_NAME, value = "btn-small-gray")
            login[0].send_keys(keys.id)
            login[1].send_keys(keys.password)
            button.click()
            break

        except:         # posso indicare anche solo un errore
            try:
                green_btn = driver.find_element(by=By.CLASS_NAME, value = "btn-large-green").text
                if green_btn == "Deposita":
                    break

            except:
                time.sleep(1)

def roulette(driver):

    while True:
        try:
            event_buttons = driver.find_elements(by=By.CLASS_NAME, value = "enable-click")
            for i in range(np.size(event_buttons)):
                event_buttons[i].find_element(by=By.CLASS_NAME, value="btn-title")
                if event_buttons[i].text == "Roulette":
                    event_buttons[i].click()
                    break
            break
                
        except:

            try:
                btn = driver.find_elements(by=By.CLASS_NAME, value="btn-close")[0]
                btn.click()

            except:
                time.sleep(2)


def click_thumbnail(driver, act, lobby):

    while True:
        try:
            thumbs = driver.find_elements(by=By.CLASS_NAME, value="game-thumb")
            for i in range(np.size(thumbs)):
                gamename = thumbs[i].find_element(by=By.CLASS_NAME, value="game-name")
                if gamename.text == lobby:
                    act.move_to_element(thumbs[i]).perform()
                    time.sleep(1)
                    giocabutton = driver.find_elements(by=By.CLASS_NAME, value="btn-large-green")
                    giocabutton[1].click()
                    break
            break

        except:
            time.sleep(2)


def enter_frame(driver, frame):

    while True:
        try:
            gameframe = driver.find_element(by=By.ID, value=frame)
            driver.switch_to.frame(gameframe)
            break

        except:
            time.sleep(2)

    
def closebutton(driver):

    while True:
        try:
            closebutton = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[3]/div[1]/div/div[1]/div[2]/div[11]/div[1]/div[2]/div/div[3]')
            # closebutton = driver.find_element(by=By.CLASS_NAME, value='close-button')
            closebutton.click()
            break

        except:
            time.sleep(2)


def playtech_roulette(driver):

    while True:
        try:
            slides = driver.find_elements(by=By.CLASS_NAME, value="lobby-category-item__wrapper")
            slides[2].click()
            break

        except:
            time.sleep(2)


def acquire_views(driver):

    while True:
        try:
            try:
                view_switcher = driver.find_element(by=By.CLASS_NAME, value="grid-btn.grid-btn_small")
            except:
                try:
                    view_switcher = driver.find_element(by=By.CLASS_NAME, value="grid-btn.grid-btn_medium")
                except:
                    try:
                        view_switcher = driver.find_element(by=By.CLASS_NAME, value="grid-btn.grid-btn_large")
                    except:
                        print("Error! Could not retrive View Switcher Button...")
                        driver.quit()

            views = view_switcher.find_elements(by=By.TAG_NAME, value="rect")
            wideview = views[5]
            normalview = views[4]
            narrowview = views[3]
            break

        except:
            time.sleep(2)

    return wideview, normalview, narrowview


def get_tables_play(driver):

    try:
        tables = driver.find_elements(by=By.CLASS_NAME, value="lobby-tables__item")
        # in alternativa dovrei fare drag&drop della barretta

    except:
        print("Error! There was a problem while reading the tables.")

    return tables


def get_tables_evo(driver):

    try:
        tables = driver.find_elements(by=By.CLASS_NAME, value="GridListItem--b95c7")
        # in alternativa dovrei fare drag&drop della barretta

    except:
        print("Error! There was a problem while reading the tables.")

    return tables


def get_lobbyname_play(lobby):

    try:
        lobbyname = lobby.find_element(by=By.CLASS_NAME, value="lobby-table__name-container").text

    except:
        lobbyname = "null"

    return lobbyname


def get_lobbyname_evo(lobby):

    try:
        lobbyname = lobby.find_element(by=By.CLASS_NAME, value="Typography--46b8a.Typography_xs_subtitle1--c55ab.Typography_md_h6--ebc04.Typography_xl_h5--c919c.bold--9a1d2.colorPrimary--5a57c.ellipsisModeOneLine--eb3a6").text

    except:
        lobbyname = "null"

    return lobbyname


def get_lobbyhistory(lobby):

    valid_history = 0

    try:
        lobbyhistory = lobby.find_element(by=By.CLASS_NAME, value="roulette-historyfOmuwAaXbwHRa3HTIjFP.roulette-history_lobbyDxuTPpg3FmAO6mbqrAe7").text

    except:
        lobbyhistory = "null"

    if nav.check_lobbyhistory(lobbyhistory):
        valid_history = 1
        lobbyhistory = lobbyhistory.split('\n')
        for j in range(np.size(lobbyhistory)):
            lobbyhistory[j] = int(lobbyhistory[j])
        lobbyhistory = np.array(lobbyhistory)

    return lobbyhistory, valid_history


def check_lobbyhistory(lobbyhistory):

    flag = 1

    for i in keys.deprecated_histories:
        if lobbyhistory == i:
            flag = 0

    return flag


def enter_amount(driver, balance):

    while True:
        try:
            input_field = driver.find_element(by=By.CLASS_NAME, value="modal-input-text")
            input_field.send_keys(balance)
            break

        except:
            time.sleep(2)


def get_balance(driver, bot, message):

    while True:
        try:
            balance = driver.find_elements(by=By.CLASS_NAME, value="fit-container__contentl2noRBpTnyQVMFpTYsrN")[0].text
            balance = float(balance.split(" ")[1].replace(",", "."))
            balance_str = 'Your balance is currently: €{:.2f}'.format(balance)
            bot.send_message(message.chat.id, balance_str)
            break

        except:
            time.sleep(2)

    return balance


def confirm_amount(driver):

    while True:
        try:
            confirm_btn = driver.find_element(by=By.CLASS_NAME, value="modal-footer-btn.modal-footer-btn_resolve.modal-footer-btn_full")
            confirm_btn.click()
            break
        
        except:
            time.sleep(2)

def confirmation_code(driver):

    while True:
        try:
            confirm_code_btn = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[3]/div[1]/div/div[1]/div[2]/div[11]/div/div[2]/div[2]/button')
            confirm_code_btn.click()
            break
        
        except:
            time.sleep(2)


def get_chips(driver):

    while True:
        try:
            chips = driver.find_elements(by=By.CLASS_NAME, value="chip.arrow-slider__element")
            chips[0].click()
            break
        
        except:
            time.sleep(2)

    return chips, chips[0], chips[1], chips[2], chips[3], chips[4]


def get_dozens(driver):

    while True:
        try:
            first_dozen = driver.find_element(by=By.CLASS_NAME, value="roulette-table-cell.roulette-table-cell_side-first-dozen.roulette-table-cell_group-dozen")
            second_dozen = driver.find_element(by=By.CLASS_NAME, value="roulette-table-cell.roulette-table-cell_side-second-dozen.roulette-table-cell_group-dozen")
            third_dozen = driver.find_element(by=By.CLASS_NAME, value="roulette-table-cell.roulette-table-cell_side-third-dozen.roulette-table-cell_group-dozen")
            break
        
        except:
            time.sleep(2)

    return first_dozen, second_dozen, third_dozen


def get_timer(driver):

    while True:
        try:
            timer = driver.find_element(by=By.CLASS_NAME, value="round-timers.round-timers_center-video")
            print(timer.text)
            break

        except:
            time.sleep(1)

    return timer


def get_returntolobby(driver):

    while True:
        try:
            bottom_buttons = driver.find_element(by=By.CLASS_NAME, value="sidebar__bottom-buttons")
            returntolobby = bottom_buttons.find_elements(by=By.CLASS_NAME, value="sidebar-buttons__item")[1]
            returntolobby.click()
            break

        except:
            time.sleep(2)


def bid_dozen(driver, dozen, chip):

    bid = 0

    while get_timer(driver) == "":
        time.sleep(1)    

    while True:
        try:
            chip.click()
            dozen.click()
            bid = 1
            break
        
        except:
            time.sleep(1)

    return bid


def aafk(driver, table):

    print("Trying to enter a game...")

    while True:
        try:
            table.click()
            time.sleep(1)

            amount = str(3 + lib.randomint(3))
            nav.enter_amount(driver, amount)
            time.sleep(0.2)

            nav.confirm_amount(driver)
            time.sleep(0.3)

            nav.confirmation_code(driver)
            time.sleep(1)

            nav.get_returntolobby(driver)

            break

        except:
            time.sleep(2)


def remove_ads(driver):

    tries = 1

    while True:

        try:
            btn = driver.find_elements(by=By.CLASS_NAME, value="btn-close")[0]
            btn.click()
            break

        except:
            tries += 1
            if tries > keys.max_nav_tries:
                break
            time.sleep(2)


def aafk_exit(driver, act):

    print("Performing AAFK Procedure...")
    tries = 1

    while True:
        try:
            driver.switch_to.parent_frame()      # switches out of gameframe
            exit_btn = driver.find_element(by=By.CLASS_NAME, value="btn-close")
            exit_btn.click()

            break

        except:
            tries += 1
            if tries > keys.max_nav_tries:
                print("Error! - Could not find the Exit Button!")
                break
            time.sleep(2)

    if tries <= keys.max_nav_tries:
        nav.click_thumbnail(driver, act, keys.playtech_entering_lobby)
        time.sleep(1)
        nav.enter_frame(driver, keys.playtech_frame)
        time.sleep(1)
        nav.closebutton(driver)
        time.sleep(1)
        nav.playtech_roulette(driver)
        
        print("Restarting the iterations...")
        time.sleep(2)

    else:
        print("There has been an error in the AAFK Procedure!")



def playtech_navigation(driver, bot, message):

    # Open Url
    driver.get(keys.url)
    
    # Login #
    nav.login(driver)

    # Roulette SubSection Click & Remove Possible Ads #
    time.sleep(2)       # loading time...
    nav.roulette(driver)

    # Roulette Italiana Click #
    time.sleep(1)
    act = ActionChains(driver)
    nav.click_thumbnail(driver, act, keys.playtech_entering_lobby)

    # Exit to Summary Screen -> Switch to iframe with ID = gameFrame #
    time.sleep(1)
    nav.enter_frame(driver, keys.playtech_frame)

    summ_prep_msg = bot.send_message(message.chat.id, "preparing summary...")

    # Close Button #
    time.sleep(1)
    nav.closebutton(driver)
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

    time.sleep(1)

    return driver, act, summ_prep_msg, balance, normalview, narrowview, wideview


def playtech_navigation_test(driver):

    # Open Url
    driver.get(keys.url)

    # Login #
    nav.login(driver)

    # Roulette SubSection Click & Remove Possible Ads #
    time.sleep(2)       # loading time...
    nav.roulette(driver)

    # Roulette Italiana Click #
    time.sleep(1)
    act = ActionChains(driver)
    nav.click_thumbnail(driver, act, keys.playtech_entering_lobby)

    # Exit to Summary Screen -> Switch to iframe with ID = gameFrame #
    time.sleep(1)
    nav.enter_frame(driver, keys.playtech_frame)

    # Close Button #
    time.sleep(1)
    nav.closebutton(driver)

    # Change Slide to Roulette #
    time.sleep(2)
    nav.playtech_roulette(driver)

    # Acquire Views #
    time.sleep(2)
    wideview, normalview, narrowview = nav.acquire_views(driver)
    normalview.click()
    narrowview.click()
    wideview.click()

    time.sleep(1)

    return driver, act, normalview, narrowview, wideview


def playtech_navigation_restart(driver, bot, message):

    # Close Previous Driver
    driver.close()
    time.sleep(1)

    # Create Driver #
    driver = webdriver.Chrome(keys.chrome_path, options=keys.chrome_options)
    driver.get(keys.url)

    # Login #
    nav.login(driver)

    # Roulette SubSection Click & Remove Possible Ads #
    time.sleep(2)       # loading time...
    nav.roulette(driver)

    # Roulette Italiana Click #
    time.sleep(1)
    act = ActionChains(driver)
    nav.click_thumbnail(driver, act, keys.playtech_entering_lobby)

    # Exit to Summary Screen -> Switch to iframe with ID = gameFrame #
    time.sleep(1)
    nav.enter_frame(driver, keys.playtech_frame)

    # Close Button #
    time.sleep(1)
    nav.closebutton(driver)

    # Change Slide to Roulette #
    time.sleep(2)
    nav.playtech_roulette(driver)

    # Acquire Views #
    time.sleep(2)
    wideview, normalview, narrowview = nav.acquire_views(driver)
    wideview.click()

    time.sleep(1)

    return driver, act, normalview, narrowview, wideview


def evolution_navigation(driver):

    driver.get(keys.url)

    # Login #
    nav.login(driver)

    # Roulette Slide SubSection Click & Remove Possible Ads #
    time.sleep(2)       # loading time...
    nav.roulette(driver)

    # Roulette Lobby Click #
    time.sleep(1)
    act = ActionChains(driver)
    nav.click_thumbnail(driver, act, keys.evolution_entering_lobby)

    # Exit to Summary Screen -> Switch to iframe with ID = iframe #
    time.sleep(1)
    nav.enter_frame(driver, keys.playtech_frame)


    return driver, act


def click_afk_button(driver):

    tries = 0

    while tries < keys.max_nav_tries:

        try:
            afk_btn = driver.find_element(by=By.CLASS_NAME, value = 'modal-footer-btn.modal-footer-btn_resolve.modal-footer-btn_full')
            afk_btn.click()
            break

        except:
            time.sleep(1)
            tries += 1


def last_hope(driver, bot, message):

    managed = 0

    # Try to close AFK Button
    try:
        nav.click_afk_button(driver)
        managed = 1

    except:
        # Last Attempt to Try to save the Program
        try:
            driver, act, normalview, narrowview, wideview = nav.playtech_navigation_restart(driver, bot, message)
            managed = 1

        except:
            managed = 0

    return managed


def switch_to_windowframe(driver, window, frame):

    driver.switch_to.window(window)
    nav.enter_frame(driver, frame)