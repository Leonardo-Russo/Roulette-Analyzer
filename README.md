# Online Roulette Analysis Bot

This project is an example of the application of Python scripting, data analysis, and bot creation to analyze online roulette tables. This script continually analyzes data from a number of online roulette tables, and once specific criteria are met, it interacts with the game.

**Please note** that the focus of this project is the technical challenges of automating the process and interpreting the data, not encouraging gambling or cheating. The aim is to illustrate how software can be used to automate data collection and interpretation in real-world scenarios. 

## Features

- **Data Collection:** The script scrapes data from multiple online roulette tables. 
- **Data Analysis:** Analysis is conducted to identify tables that meet specific criteria.
- **Automated Interaction:** Once the criteria are met, the script can automatically place a bet on one of the three dozens.
- **Telegram Bot Interface:** A Telegram bot is used as an interface for user interaction. The bot allows users to easily check the status and modify options. It also reports all the numbers extracted from all tables.

## Technologies Used

- Python: The main programming language used in this project.
- Python Libraries: Libraries such as BeautifulSoup for web scraping, and python-telegram-bot for the Telegram bot interface.
- Telegram: Platform used for the bot interface.
  
## Future Improvements

Future updates may focus on refining the data analysis aspect of the script, or expanding the functionality of the Telegram bot interface.

---

## Disclaimer

This project is created for educational and demonstration purposes only. It should not be used for any illegal activities or any activities against the terms of service of any websites it interacts with. The creator of this project is not responsible for any misuse or any potential losses.

---
### Bidding Scheme

| n° | Bid | Loss | Win | Profit |
| --- | --- | --- | --- | --- |
| 1 | 0.5 | 0.5 | 1.5 | 1 |
| 2 | 1 | 1.5 | 3 | 1.5 |
| 3 | 2 | 3.5 | 6 | 2.5 |
| 4 | 4 | 7.5 | 12 | 4.5 |
| 5 | 8 | 15.5 | 24 | 8.5 |
| 6 | 16 | 31.5 | 48 | 16.5 |
| 7 | 32 | 63.5 | 96 | 32.5 |
| 8 | 64 | 127.5 | 192 | 64.5 |
| 9 | 128 | 255.5 | 384 | 128.5 |
| 10 | 256 | 511.5 | 768 | 256.5 |
