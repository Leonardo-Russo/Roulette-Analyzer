from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

API_KEY = "YOUR_API_KEY"
N_storage = 11
wait_max = 20
tmax = 600

iterations_dt = 1       # Interval between Iterations

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

accepted_lobbies = {'Roulette Italiana', 'American Roulette', 'Deutsches Roulette', 'French Roulette', 'Triumph French Roulette', 'Greek Roulette', 'Hindi Roulette', 'Turkish Roulette', 'Triumph Roulette', 'Roulette', 'Roleta Brasileira', 'UK Roulette'}
problematic_lobbies = {}
deprecated_histories = {'', ' ', 'null'}

# n° of iterations after which perform in&out
n_afk = 50