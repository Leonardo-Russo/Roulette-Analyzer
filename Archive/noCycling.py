from dbm.ndbm import library
from idna import valid_contextj
from requests import head
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time

import numpy as np
import pandas as pd
import re

import Archive.nameparser as npsr
from library import namecheck

options = Options()
options.add_argument("disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")

def cycling():

    path = "C:\Program Files (x86)\chromedriver.exe"
    driver365 = webdriver.Chrome(path, options=options)
    driverEuro = webdriver.Chrome(path, options=options)
    driverSisal = webdriver.Chrome(path, options=options)
    driver365.minimize_window()
    driverEuro.minimize_window()
    driverSisal.minimize_window()
    url_bet365 = "https://www.bet365.it/?_h=FbIktsv5STISLB5hXbkMbQ%3D%3D#/AC/B38/C20756735/D1/E70015827/F2/"
    url_euro = "https://www.eurobet.it/it/scommesse/#!/ciclismo/it-giro-d-39-italia/"
    url_sisal = "https://www.sisal.it/scommesse-matchpoint/evento/ciclismo/giro-d-italia/giro-d-italia"
    print('Program is starting...')

    ## Esempio con Giro d'Italia ##

    ## Ciclista Vincente ##
    driver365.get(url_bet365)
    driverEuro.get(url_euro)
    driverSisal.get(url_sisal)

    ## FIND ANOTHER WAY
    # main = WebDriverWait(driver, 10).until(
    # EC.presence_of_element_located((By.CLASS_NAME, "g5-Application.widthState1.viewState1.allow-hover"))
    # )
    

    ## BET365 ##
    try:
        
        time.sleep(1)
        main = driver365.find_element(by=By.CLASS_NAME, value="g5-Application.widthState1.viewState1.allow-hover")

        event = main.find_element(by=By.CLASS_NAME, value="sph-EventHeader_Label")
        print('\n____________________________________________________________________\n\nEvent: ', event.text, '\n')

        names = main.find_elements(by=By.CLASS_NAME, value="gl-ParticipantBorderless_Name")
        odds = main.find_elements(by=By.CLASS_NAME, value="gl-ParticipantBorderless_Odds")
        entries = np.size(names)

        archive = []
        name_archive = []        
        for i in range(entries):
            names[i] = names[i].text
            odds[i] = odds[i].text
            name_archive = names[i].split()
            archive.append(name_archive)

        bet365 = pd.DataFrame(
            {
                "Name" : names,
                "Odds" : odds,
            }
        )

        df = bet365
        fullnames = names

        print(bet365)

        # print('\n___________________\n', bet365.Name[0], bet365.Odds[3])      here's how you access data

    finally:
        driver365.close()


    ## EUROBET ##
    try:
    
        time.sleep(1)
        main = driverEuro.find_element(by=By.CLASS_NAME, value="page.home-page-sport.it")

        events = main.find_elements(by=By.CLASS_NAME, value="event-name.prematch-name")
        if np.size(events) > 1:
            print('\nPlease select the Eurobet event:')
            for i in range(np.size(events)):
                print(i+1, '. ', events[i].text)

        # eventchoice = int(input())
        eventchoice = 2
        event = events[eventchoice-1].text
        print('\n____________________________________________________________________\n\nEvent: ', event, '\n')

        boxes = main.find_elements(by=By.CLASS_NAME, value="box-row-event")
        box = boxes[eventchoice-1]

        namesandodds = box.find_elements(by=By.CLASS_NAME, value="quota.two-info")
        # odds = main.find_elements(by=By.CLASS_NAME, value="gl-ParticipantBorderless_Odds")
        entries = np.size(namesandodds)

        names = []
        odds = []
        
        for i in range(entries):      # here I added the -2 since it must not consider empty slots in the page
            namesandodds[i] = namesandodds[i].text
            h = namesandodds[i].split('\n')
            if np.size(h) > 1:
                if h[1] != '1.00':
                    names.append(h[0])
                    odds.append(h[1])

        nmin = 3
        for i in range(np.size(names)):
            k, flag = namecheck(archive, nmin, names[i])
            if flag == 1:
                # print(names[i], ' should be equal to ', archive[k])
                names[i] = fullnames[k]
            # if flag == 0:
                # df.Name.append(names[i])
                # df.Name = pd.concat([df.Name, names[i]], ignore_index=True, axis=0)
            
        Euro = pd.DataFrame(
            {
                "Name" : names,
                "Odds" : odds,
            }
        )

        # zeroodds = np.zeros([entries, 1])
        # df['EuroOdds'] = zeroodds
        
        # for i in range(np.size(df.Name)):
        #     for j in range(np.size(names)):
        #         if df.Name[i] == Euro.Name[j]:
        #             df['EuroOdds'][j] = Euro.Odds[j]

        print(Euro)

        df.merge(Euro, how='outer', on='Name').reindex(df.columns, axis=1)
        
        print(df)

        



        # print('\n___________________\n', bet365.Name[0], bet365.Odds[3])      here's how you access data

    finally:
        driverEuro.close()


    # ## SISAL ##
    # try:
    
    #     time.sleep(1)
    #     main = driverSisal.find_element(by=By.CLASS_NAME, value="fr.game-detail-page.user-not-logged.is-desktop-device")

    #     events = main.find_elements(by=By.CLASS_NAME, value="d-block.text-capitalize")
    #     print('\n____________________________________________________________________\n\nEvent: ', events[0].text, '\n')

    #     # names = main.find_elements(by=By.CLASS_NAME, value="selectionButton_description__3fVPQ")
    #     # # odds = main.find_elements(by=By.CLASS_NAME, value="gl-ParticipantBorderless_Odds")
    #     # entries = np.size(namesandodds)

    #     # names = []
    #     # odds = []
        
    #     # for i in range(entries-2):      # here I added the -2 since it must not consider empty slots in the page
    #     #     namesandodds[i] = namesandodds[i].text
    #     #     h = namesandodds[i].split('\n')
    #     #     if h[1] != '1.00':
    #     #         names.append(h[0])
    #     #         odds.append(h[1])

    #     # Euro = pd.DataFrame(
    #     #     {
    #     #         "Name" : names,
    #     #         "Odds" : odds,
    #     #     }
    #     # )

    #     # print(Euro)
        
    #     # print('\n___________________\n', bet365.Name[0], bet365.Odds[3])      here's how you access data

    # finally:
        driverSisal.close()


if __name__ == '__main__':
    cycling()