from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode
from urllib.parse import quote
import requests
import operator
import time
import os
import re

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager
        
# from https://stackoverflow.com/a/32558749/6386471
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def match_manufacturer(manufacturer, match_list):
    scores = {}
    for m in match_list:
        scores[m] = 1 - levenshteinDistance(manufacturer,m)
    manufacturer = max(scores.items(), key=operator.itemgetter(1))[0]
    return manufacturer

def get_url_sel(keyword):
    options = Options()
    options.add_argument("--headless=new") # Runs Chrome in headless mode.
    options.add_argument("--no-sandbox=new") # Bypass OS security model
    options.add_argument("--disable-gpu=new") # applicable to windows os only
    options.add_argument("start-maximized=new") 
    options.add_argument("disable-infobars=new")
    options.add_argument("--disable-extensions=new")
    
    service = ChromeService(executable_path = ChromeDriverManager().install())
    driver = webdriver.Chrome(service = service, options = options) #
    driver.get('https://www.findchips.com')
    time.sleep(2)
    
    part_detail_tab = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Part Details'))).click() # Part Details search tab
    # part_detail_tab.click() # click on Part Details tab
    part_num_input = driver.find_element(By.CSS_SELECTOR, 'input#part')
    part_num_input.send_keys(keyword)
    WebDriverWait(driver,1)
    part_num_input.send_keys(Keys.ENTER)
    
    url = driver.current_url
    page = driver.page_source
    driver.close()
    return page, url

def fc_get_part_info(keyword, manufacturer):
    # params = quote(keyword + "/" + manufacture)
    # url = "https://www.findchips.com/detail/"
    info = get_url_sel(keyword)
    page = info[0]
    full_url = info[1]
    # full_url = url+params
    # print(keyword)

    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}

    # page = requests.get(full_url, headers = headers)
    # soup = bs(page.content, 'html.parser')
    soup = bs(page, features="lxml") 
    # soup_1 = bs(soup.prettify(), 'html.parser')
    # print(soup_1)
    manufacture = manufacturer.replace('.', '')
    url = "https://www.findchips.com/detail/"
    try:
        manufacturer_list = [str(x.text) for x in soup.find(class_="j-select-manufacturer").find_all('option')]
        # print(manufacturer_list)
        m_manufacturer = match_manufacturer(manufacture, manufacturer_list)
        # print(m_manufacturer)
        manufacture = m_manufacturer.replace('.', '')
        params = quote(keyword + "/" + manufacture.replace(' ', '-'))
        full_url = url+params
        page = requests.get(full_url, headers = headers)
        soup = bs(page.content, 'html.parser')
        # print(bs(soup.prettify(), 'html.parser'))
        # print(full_url)
    except:
        # print("Correct url: " + full_url)
        pass
    try:
        td1 = soup.find(lambda t: t.text.strip()=='Mounting Feature')
        td2 = td1.find_next('td')
        mounting = td2.text.strip()
        # print(mounting)
    except:
        try:
            td1 = soup.find(lambda t: t.text.strip()=='Mounting Type')
            td2 = td1.find_next('td')
            mounting = td2.text.strip()
            # print(mounting)
        except:
            mounting = None

    try:
        td3 = soup.find(lambda t: t.text.strip()=='Size Code')
        td4 = td3.find_next('td')
        case = td4.text.strip()
        # print(case)
    except:
        try:
            td3 = soup.find(lambda t: t.text.strip()=='Case Code')
            td4 = td3.find_next('td')
            case = td4.text.strip()
            # print(case)
        except:
            try:
                td3 = soup.find(lambda t: t.text.strip()=='Package Description')
                td4 = td3.find_next('td')
                case = td4.text.strip()
                # print(case)
            except:
                case = None
    return mounting, case, full_url
"""TEST CASE"""
# start_time = time.time()
# keyword = "C0603C331J5GACTU"
# manufacturer = "KEMET"
# info = fc_get_part_info(keyword, manufacturer)
# print("--- %s seconds ---" % (time.time() - start_time))