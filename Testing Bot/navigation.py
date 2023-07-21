from logging.config import valid_ident
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

    wait = WebDriverWait(driver, keys.wait_max)
    while True:
        try:
            login = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "top-menu-input-w.input-text.w126")))
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-small-gray")))
            login[0].send_keys(keys.id)
            login[1].send_keys(keys.password)
            button.click()
            break

        except:         # posso indicare anche solo un errore
            time.sleep(2)

def roulette(driver):

    wait = WebDriverWait(driver, keys.wait_max)
    while True:
        try:
            event_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "enable-click")))
            for i in range(np.size(event_buttons)):
                event_buttons[i].find_element(by=By.CLASS_NAME, value="btn-title")
                if event_buttons[i].text == "Roulette":
                    event_buttons[i].click()
                    break
            break
                
        except:
            time.sleep(2)


def thumbnails(driver, act):

    while True:
        try:
            thumbs = driver.find_elements(by=By.CLASS_NAME, value="game-thumb")
            for i in range(np.size(thumbs)):
                gamename = thumbs[i].find_element(by=By.CLASS_NAME, value="game-name")
                if gamename.text == "Roulette Italiana":
                    act.move_to_element(thumbs[i]).perform()
                    time.sleep(1)
                    giocabutton = driver.find_elements(by=By.CLASS_NAME, value="btn-large-green")
                    giocabutton[1].click()
                    break
            break

        except:
            time.sleep(2)


def gameframe(driver):

    while True:
        try:
            gameframe = driver.find_element(by=By.ID, value="gameFrame")
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


def aafk(driver, table):

    print("Trying to enter a game...")

    table.click()

    time.sleep(1)
    closebutton(driver)
    time.sleep(1)


def aafk_prov(driver, table1, table2):

    print("Trying to enter a game...")

    flag = lib.randomint(1)

    if flag:
        table1.click()
    else:
        table2.click()

    time.sleep(1)
    closebutton(driver)
    time.sleep(1)


def get_tables(driver, act):

    try:
        tables = driver.find_elements(by=By.CLASS_NAME, value="lobby-tables__item")
        # in alternativa dovrei fare drag&drop della barretta

    except:
        print("Error! There was a problem while reading the tables.")

    return tables


def get_lobbyname(lobby):

    try:
        lobbyname = lobby.find_element(by=By.CLASS_NAME, value="lobby-table__name-container").text

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


def scroll_shim(driver, object):

    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    
    driver.execute_script(scroll_by_coord)
    driver.execute_script(scroll_nav_out_of_way)


def scrolling(driver, lobby):

    driver.execute_script("window.scrollTo(0,50);")


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
            msg = "Your balance is currently: € " + str(balance)
            bot.send_message(message.chat.id, msg)
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
