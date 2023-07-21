from idna import valid_contextj
from requests import head
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import numpy as np
import pandas as pd

## NOTES: ##
# The error related to USB device (...) can be neglected, it is just a bug of the Chrome driver.
# I should fix the better formulation to scrape.
# The n° of teams depends greatly on the sport, in general it is = partecipants + 1

# I want to focus on the Player Points

### Legend:
# 1 - Mercati Principali
# 3 - Prospetto Giocatori

def noBet():

    # define path to the chromedriver
    path = "C:\Program Files (x86)\chromedriver.exe"

    driver1 = webdriver.Chrome(path)
    driver3 = webdriver.Chrome(path)

    url1 = "https://www.bet365.it/?_h=FbIktsv5STISLB5hXbkMbQ%3D%3D#/AC/B18/C20604387/D19/E14332674/F19/"
    url3 = "https://www.bet365.it/?_h=FbIktsv5STISLB5hXbkMbQ%3D%3D#/AC/B18/C20604387/D19/E14342681/F19/I43/"

    print("\nLadies and Gentlemen, the program is starting...\n", "_"*50, "\n\n")

    ### Mercati Principali ###
    driver1.get(url1)

    try:
        ## this is the more correct way to scrape, but it doesn't work :(
        # main = WebDriverWait(driver, 10).until(
        # EC.presence_of_element_located((By.CLASS_NAME, "g5-Application.allow-hover.widthState1.viewState1"))
        # )

        time.sleep(1)

        event = driver1.find_element(by=By.CLASS_NAME, value="sph-EventHeader_Label")
        print(event.text)

        main_markets = driver1.find_element(by=By.CLASS_NAME, value="g5-Application.allow-hover.widthState1.viewState1")

        navbars = main_markets.find_elements(by=By.CLASS_NAME, value="sph-MarketGroupNavBarButton")
        n_navbars = np.size(navbars)        # n° of navbars

        teams = main_markets.find_elements(by=By.CLASS_NAME, value="gl-MarketColumnHeader")
        n_teams = 3                         # n° of teams, in basketball it is always 3
        teams = teams[0:n_teams]

        # handicap_quote = driver.find_elements(by=By.CLASS_NAME, value="sab-ParticipantCenteredStackedOTB_Handicap")

        # print(event.text)
        # for i in range(n_navbars):
        #     print(navbars[i].text)
        # for i in range(n_teams):
        #     print(teams[i].text)

    finally:
        driver1.close()


    ### Prospetto Giocatori ###
    driver3.get(url3)

    try:

        time.sleep(1)

        event = driver3.find_element(by=By.CLASS_NAME, value="sph-EventHeader_Label")
        print(event.text)

        main_players = driver3.find_element(by=By.CLASS_NAME, value="g5-Application.widthState1.viewState1.allow-hover")
        players_points = main_players.find_elements(by=By.CLASS_NAME, value="srb-ParticipantLabelWithTeam_Name")
        points_line = main_players.find_elements(by=By.CLASS_NAME, value="gl-ParticipantCenteredStacked_Handicap")
        points_odds = main_players.find_elements(by=By.CLASS_NAME, value="gl-ParticipantCenteredStacked_Odds")

        points_line_low = main_players.find_elements(by=By.CLASS_NAME, value="gl-ParticipantCenteredStacked_Handicap")
        points_odds_low = main_players.find_elements(by=By.CLASS_NAME, value="gl-ParticipantCenteredStacked_Odds")
        # here I need to expand the page, I need to watch the tutorial on how to navigate


        n_players = np.size(players_points)
        # n_line = np.size(points_line)
        # n_points_odds = np.size(points_odds)

        # size check
        # print("\nSize Check:\nSize of Players: ", n_players,"\nSize of Line: ", n_line, "\nSize of Odds: ", n_points_odds)

        for i in range(n_players):
            print(players_points[i].text, " con linea a ", points_line[i].text, "\nOver: ", points_odds[i].text, "\nUnder: ", points_odds[i+n_players].text, "\n\n")

        # print(main_players.text)

    finally:
        driver3.close()

    
if __name__ == '__main__':
    noBet()