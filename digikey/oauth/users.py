import json
import os
from pathlib import Path
import typing as t

"""
Selenium for user login
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
logging.captureWarnings(True)
logger = logging.getLogger(__name__)
import time
from random import randint

from digikey.exceptions import DigikeyUserException
from utils.utils import encode_text, decode_text, is_obfuscated
from digikey.constants import AUTH_URL_V1_PROD, AUTH_URL_V1_SB, TOKEN_URL_V1_PROD, TOKEN_URL_V1_SB, USER_AGENT

USER_STORAGE = 'digikey_user.json'

class SelLogin():
    
    def __init__(self, browser):
        self.browser = browser
        
    def chrome_options(self, experimental_opt=True):
        options = ''
        if self.browser != 'chrome':
            return("Unable to initiate Chrome options")
        else:
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={USER_AGENT}')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--incognito')
            # options.add_argument('--headless')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-extensions")
            if experimental_opt:
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                options.add_experimental_option('useAutomationExtension', False)
        return options
            
    def set_capabilities(self):
        capabilities = ''
        if self.browser == 'chrome':
            capabilities = DesiredCapabilities.CHROME.copy()
        elif self.browser == 'firefox':
            capabilities = DesiredCapabilities.FIREFOX.copy()
        elif self.browser == 'ie':
            capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
        else:
            raise ValueError("Driver failed because there are no valid browser.")
        capabilities['acceptInsecureCerts'] = True
        return capabilities
    
    def get_driver(self, path=None):
        driver = None
        if self.browser != 'chrome':
            raise ValueError('BROWSER must be set to CHROME')
        if path == None:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                      options=self.chrome_options(),
                                      desired_capabilities=self.set_capabilities())
        else:
            try:
                logger.debug("Initiating ChromeDriver from PATH")
                service = Service(path)
                driver = webdriver.Chrome(service=service,
                                          options=self.chrome_options(),
                                          desired_capabilities=self.set_capabilities())
            except Exception as e:
                logger.error("Unable to setup driver: {}".format(e))
        return driver
    
    def GET_code(self, auth_url, username, password):
        driver = self.get_driver()
        driver.get(auth_url)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": USER_AGENT})
        
        randtime = randint(2,8)
        wait = WebDriverWait(driver, randtime)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'logo-frame')))
        logger.debug("Logging in as: {}".format(username))
        
        user_field = driver.find_element(By.CSS_SELECTOR, 'input#username')
        pass_field = driver.find_element(By.CSS_SELECTOR, 'input#password')
        submit_button = driver.find_element(By.CSS_SELECTOR, 'a#signOnButton')
        time.sleep(2)
        user_field.send_keys(username)
        pass_field.send_keys(password)
        time.sleep(1)
        submit_button.click()
        time.sleep(1)
        
        code_url = driver.current_url
        logger.debug("Successful Authentication URL: {}".format(code_url))
        driver.close()
        return code_url

class DigikeyAuth:
    ''' Digi-Key Authentication properties for a single user '''
    def __init__(self, user_dictionary):
        self._user = user_dictionary # dictionary
        
    @property
    def user_index(self):
        self._user_idx = self._user.get('user_id')
        return self._user_idx
    
    @property
    def redirect_uri(self):
        self._redirect_uri = self._user.get('redirect_uri')
        return self._redirect_uri
    
    @property
    def username(self):
        self._username = self._user.get('username')
        return self._username
    
    @property
    def password(self):
        self._password = self.decode_data(self._user.get('password'))
        return self._password
        
    @property
    def client_id(self):
        self._client_id = self.decode_data(self._user.get('client_id'))
        return self._client_id
    
    @property
    def client_secret(self):
        self._client_secret = self.decode_data(self._user.get('client_secret'))
        return self._client_secret
    
    def __repr__(self):
        user_display = f'''Current Digi-Key user:
---------------------
UserIDX: {self.user_index}
Email: {self.username}
Password: {self.password}
Client ID: {self.client_id}
Client Secret: {self.client_secret}
        '''
        return '{}'.format(user_display)
    
    def decode_data(self, data_str):
        # check if the text is obfuscated
        if is_obfuscated(data_str) is True:
            data_str = decode_text(data_str)
        else:
            pass
        return data_str
        
# user_storage_path: t.Optional[str]=None,        
class User:
    def __init__(self,
                 user_storage_path: t.Optional[str] = None,
                 a_id: t.Optional[str] = None, 
                 a_secret: t.Optional[str] = None, 
                 a_username: t.Optional[str] = None, 
                 a_password: t.Optional[str] = None, 
                 a_callback: t.Optional[str] = None
                ):
        self._user_storage_path = None
        self._user_file = None
        self._uidx = None
        if user_storage_path is not None:
            current_dir = os.path.dirname(os.path.abspath(user_storage_path))
            cache_dir = os.path.join(current_dir, 'data')
            self._user_storage_path = Path(cache_dir)
            self._user_file = self._user_storage_path.joinpath(USER_STORAGE)
            logger.debug(f'Using {self.user_file}.')
        
        if all(creds is not None for creds in [a_id, a_secret, a_username, a_password, a_callback]):
            self._id = a_id
            self._secret = a_secret
            self._username = a_username
            self._password = a_password
            self._callback = a_callback
            self._uidx = a_username.split('@')[0]
            logger.debug(f'Initiating instance Digikey credentials.')
        else:
            logger.debug(f'No DigiKey Client instance found. Proceeding with only the USER_STORAGE file.')
        if user_storage_path is None and self._uidx is None:
            raise ValueError(
                'STORAGE_PATH or DIGIKEY CLIENT CREDENTIALS must be set. '
                'You may upload a json user file or enter client credentials in the client. '
            )
        
    def secure_data(self, data_str):
        # check if the text is obfuscated
        if is_obfuscated(data_str) is False:
            data_str = encode_text(data_str)
        else:
            pass
        return data_str
    
    def obfuscate_user_file(self):
        with open(self._user_file, 'r') as file:
            user_list = json.load(file) # list of digikey users
        if len(user_list) > 0:
            secured_ulist = []
            for user in user_list:
                keys_to_obfuscate = ['password', 'client_id', 'client_secret']
                secured_user = {}
                for key, value in user.items():
                    if key in keys_to_obfuscate: 
                        secured_user[key] = self.secure_data(value)
                    else:
                        secured_user[key] = value
                secured_ulist.append(secured_user)
        with open(self._user_file, 'w') as writer:
            json.dump(secured_user_list, writer, indent=4, separators=(',',': '))
             
    def get_user(self, user_id=None) -> DigikeyAuth:
        current_user = None
        if self._uidx is not None:
            user_id = self._uidx
            instance_user = {'user_id': user_id,
                             'redirect_uri': self._callback,
                             'username': self._username,
                             'password': self.secure_data(self._password),
                             'client_id': self.secure_data(self._id),
                             'client_secret': self.secure_data(self._secret)
                            }
            current_user = DigikeyAuth(instance_user)
        else:
            with open(self._user_file, 'r') as file:
                try:
                    user_list = json.load(file) # list of digikey users
                except JSONDecodeError:
                    raise JSONDecodeError("Error with file")
                except FileNotFoundError:
                    raise FileNotFoundError("File not found")
                except Exception as e:
                    raise e
            if len(user_list) > 0:
                if user_id is None: # default
                    first_user = user_list[0]
                    current_user = DigikeyAuth(first_user) # take the first if user_id is None
                elif isinstance(user_id, int): # get the user by index
                    u_index = user_id
                    current_user = DigikeyAuth(user_list[u_index])
                else: # search user by str
                    for user in user_list:
                        if user['user_id'] == user_id:
                            current_user = DigikeyAuth(user)
                        else:
                            raise DigikeyUserException(f"{user_id} not found in {self._user_file}.")
            else:
                raise DigikeyUserException("User storage is empty")
        return current_user
    
    def save_new_user(self):
        if self._user_file is None and self._uidx is None:
            raise OSError("User storage path or client credentials must be set.")
        _user_id = self._uidx
        _redirect_uri = self._callback
        _username = self._username
        _password = self._password
        _client_id = self._id
        _client_secret = self._secret
        
        logger.debug("/n***PLEASE KEEP DIGI-KEY LOGIN INFO PRIVATE.\nPASSWORD, CLIENT ID, AND CLIENT SECRET WILL BE HIDDEN.***")    
        
        user_data = {
            'user_id': _user_id,
            'redirect_uri': _redirect_uri,
            'username': _username,
            'password': self.secure_data(_password),
            'client_id': self.secure_data(_client_id),
            'client_secret': self.secure_data(_client_secret)
        }
        logger.debug(f"Successfully created new Digikey client dictionary. Appending to '{self._user_file}'.")
        self.append_user_to_file(user_data, self._user_file)
    
    def append_user_to_file(self, user_auth, user_file):
        if not os.path.exists(user_file):
            # if file doesn't exist, we'll make a new one
            with open(user_file, 'w') as userjson:
                users_data = [user_auth] # converting the dictionary into list of dictionary
                json.dump(users_data, userjson, indent=4)
        else:
            with open(user_file) as userjson:
                try:
                    users_data = json.load(userjson) # load user list
                    users_data.append(user_auth) # add the new user to the list
                    # print(users_data) # debug
                    with open(user_file, 'w') as newjson:
                        # Overwrite the file with the list w/ new user data
                        json.dump(users_data, newjson, indent=4, separators=(',',': '))
                except JSONDecodeError:
                    # if the file exists but is empty, we'll add the new user data in it
                    logging.debug("The file exists and is empty: adding new user")
                    with open(user_file, 'w') as newjson:
                        users_data = [user_auth]
                        json.dump(users_data, newjson, indent=4, separators=(',',': '))
        logger.debug("Success, added New Digi-Key user.")
    
    def set_digikey_env(self, user=None, sandbox=False):
        """ sets the environment variables """
        if user is None:
            user = self.get_user()
        elif isinstance(user, str) or isinstance(user, int):
            user = self.get_user(user)
        else:
            raise TypeError(f"{user} is not valid. Please enter correct user type (hint: str or int)")
                
        # set DIGIKEY_CLIENT_ID'
        os.environ['DIGIKEY_CLIENT_ID'] = user.client_id
        # set DIGIKEY_CLIENT_SECRET
        os.environ['DIGIKEY_CLIENT_SECRET'] = user.client_secret
        # set DIGIKEY_USERNAME
        os.environ['DIGIKEY_USERNAME'] = user.username
        # set DIGIKEY_PASSWORD
        os.environ['DIGIKEY_PASSWORD'] = user.password
        # set REDIRECT_URL
        os.environ['REDIRECT_URL'] = user.redirect_uri
        # set DIGIKEY_STORAGE_PATH
        os.environ['DIGIKEY_STORAGE_PATH'] = self._user_storage_path
     
        # set DIGIKEY_SANDBOX if sandbox is desired
        if sandbox:
            os.environ['DIGIKEY_SANDBOX'] = True
        else:
            os.environ['DIGIKEY_SANDBOX'] = False
            
        logger.debug("Set DIGIKEY environment variables.")
        

        