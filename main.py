from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas
import datetime as dt
import pyautogui as pag



options = Options()

# options.gpu = False
prefs = {
    "download.default_directory": "F:\Python100\Portfolio projects\TradingView_automation", #directory to save csv file.
    "download.prompt_for_download": False,
    "safebrowsing.enabled": False,
}

options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
# options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
user_agent =  ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 '
               'Safari/537.36')
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--disable-infobars')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
service = Service(executable_path="F:\Python100\Portfolio projects\TradingView_automation\chromedriver.exe") # path to your chromedriver application
desired = options.to_capabilities()
desired['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(service=service, options=options, desired_capabilities=desired)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                     'Chrome/96.0.4664.45 Safari/537.36'})

driver.get('https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050')

time.sleep(5)

driver.delete_all_cookies()


# ______Auto GUI CSV Download______
pag.moveTo(107, 192, 2, pag.easeOutQuad)
pag.leftClick()

pag.sleep(5)

pag.moveTo(20, 51, 1, pag.easeOutQuad)
pag.leftClick()

print(pag.position())
pag.sleep(5)

pag.moveTo(1211, 529, 2, pag.easeOutQuad)
pag.leftClick()


time.sleep(5)


# # WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div/section/div/div/div/div"
# #                                                                      "/div[1]/div/div/div/div[2]/div/div["
# #                                                                      "3]/div/ul/li/a")))
# # link = driver.find_element(By.XPATH, '/html/body/div[9]/div/section/div/div/div/div/div[1]/div/div/div/div['
# #                                      '2]/div/div[3]/div/ul/li/a')
# # # driver.execute_script("arguments[0].click();", link)
# # link.click()
# #
# # time.sleep(10)


# _______handling CSV file_______
df = pandas.read_csv(f'MW-NIFTY-50-{dt.datetime.now().strftime("%d-%B-%Y")}.csv')

col = list(df.columns)
for i in range(len(col)):
    col[i] = col[i].strip('\n').strip(' ')

df.columns = col
df.drop(['CHNG'], axis=1, inplace=True)
df.rename(columns={'%CHNG': 'CHNG'}, inplace=True)
print(df.CHNG)
i = df[df.CHNG == "-"].index
df.drop(i, axis=0, inplace=True)
print(df.loc[df.CHNG == "-"])
df.CHNG = df.CHNG.astype(float)
df = df.query("CHNG > 1.00 | CHNG < -1.00")
stocks = ','.join(str(e) for e in df['SYMBOL'].tolist())
print(stocks)

# _______setting up Trading view_______

driver.get('https://in.tradingview.com/')

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[3]/button[1]"))).click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[6]/div/span/div[1]/div/div/div[1]"))).click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]"))).click()

email = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[1]/div[1]/input")
email.send_keys("") # Username

password = driver.find_element(By.XPATH,
                               "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[2]/div[1]/input")
password.send_keys("") # Password

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[5]/div[2]/button"))).click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[3]/div[3]/div[2]/div[1]/button"))).click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[7]/div[2]/span/div[1]/div/div/div/a"))).click()

time.sleep(5)

bts = driver.find_elements(By.CLASS_NAME, "removeButton-Zl3ogIKX")
for i in range(7, len(bts)):
    driver.implicitly_wait(10)
    driver.execute_script("arguments[0].click();", bts[i])

driver.implicitly_wait(10)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[1]"))).click()


add_stocks = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/div/div[2]/div/input")
add_stocks.send_keys(stocks)
add_stocks.send_keys(Keys.ENTER)