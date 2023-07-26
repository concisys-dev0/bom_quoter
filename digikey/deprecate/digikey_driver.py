from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from random import randint
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36"

# Automation setup
def driver_setup(path=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={USER_AGENT}') # <- assign user-agent
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--incognito') #incognito
    # chrome_options.add_argument('--headless') # no display
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptInsecureCerts'] = True
    
    if path == None:
        # print('No PATH to chromedriver.exe. Inititating ChromeDriverManager...')
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=chrome_options, 
            desired_capabilities=capabilities)
    else:
        try:
            print('Initiation chromedriver.exe from PATH')
            service = Service(path)
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), 
                options=chrome_options, 
                desired_capabilities=capabilities)
        except:
            print('Select correct path to the chromebrowser driver or leave the parameter empty')
    return driver

def user_login(auth_url, username, password):
    browser = driver_setup()
    browser.get(auth_url)
    time.sleep(randint(2,10))
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": USER_AGENT})
    wait = WebDriverWait(browser, 5)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'logo-frame')))
    print("Logging in. Please wait..")
    user_field = browser.find_element(By.CSS_SELECTOR, 'input#username')
    pass_field = browser.find_element(By.CSS_SELECTOR, 'input#password')
    submit_button = browser.find_element(By.CSS_SELECTOR, 'a#signOnButton')
    time.sleep(1)
    user_field.send_keys(username)
    pass_field.send_keys(password)
    time.sleep(1)
    submit_button.click()
    time.sleep(2)
    auth_code_url = browser.current_url
    browser.quit()
    return auth_code_url