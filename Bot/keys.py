from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

API_KEY = "YOUR_API_KEY"
N_max_display = 15          # Default Maximum Display Size
N_max_dzn = 15              # Default Dozen Check Maximum Size
N_max_colors = 10           # Default Color Check Maximum Size
N_max_evorodd = 10          # Default Even or Odd Check Maximum Size
n_afk = 25                  # n° of iterations after which perform AAFK
n_reboot = 500              # n° of iterations after which reboot the program
wait_max = 2
tmax = 600

iterations_dt = 0.1       # Interval between Iterations

chrome_options = ChromeOptions()
chrome_options.add_argument("disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--headless")
# chrome_options.add_argument(f'--user-data-dir={os.getenv("LOCALAPPDATA")}\\Google\\Chrome\\User Data')

firefox_options = FirefoxOptions()
firefox_options.add_argument("disable-dev-shm-usage")
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--start-maximized")

url = "https://livecasino.planetwin365.it/"
chrome_path = "C:\Program Files (x86)\chromedriver.exe"
firefox_path = "C:\Program Files (x86)\geckodriver.exe"

id = "YOUR_ID"
password = "YOUR_PASSWORD"

accepted_lobbies = {'Roulette Italiana', 'Prestige Roulette', 'Speed Roulette', 'American Roulette', 'French Roulette', 'Auto Roulette', 'Arabic Roulette', 'Bucharest Roulette', 'Deutsches Roulette', 'Greek Roulette', 'Hindi Roulette', 'Nederlandstalige Roulette', 'Roleta Brasileira', 'Turkish Roulette', 'UK Roulette'}
# accepted_lobbies = {'Roulette Italiana', 'Prestige Roulette', 'American Roulette', 'French Roulette', 'Arabic Roulette', 'Bucharest Roulette', 'Deutsches Roulette', 'Greek Roulette', 'Hindi Roulette', 'Nederlandstalige Roulette', 'Roleta Brasileira', 'Turkish Roulette', 'UK Roulette'}
accepted_lobbies_afk = {'Roulette Italiana', 'American Roulette', 'UK Roulette'}
accepted_lobbies_toscroll = {'Roulette Italiana', 'American Roulette', 'Auto Roulette', 'Deutsches Roulette', 'Hindi Roulette', 'UK Roulette'}
problematic_lobbies = {}
deprecated_histories = {'', ' ', 'null'}

reds = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
blacks = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

# n° of tries to do navigation tasks
max_nav_tries = 20


# other values
playtech_entering_lobby = "Roulette Italiana"
evolution_entering_lobby = "Roulette Lobby"
playtech_frame = "gameFrame"
evolution_frame = "iframe"