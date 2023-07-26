from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
import json
from json.decoder import JSONDecodeError
import webbrowser
import schedule
import time
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open_new
import typing as t

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)
from digikey.oauth.users import SelLogin
from utils.utils import *
from digikey.exceptions import DigikeyOauthException
from digikey.constants import TOKEN_STORAGE, AUTH_URL_V1_PROD, AUTH_URL_V1_SB, TOKEN_URL_V1_PROD, TOKEN_URL_V1_SB

logger = logging.getLogger(__name__)
# REDIRECT_URL = "https://localhost/"
CACHE_DIR = Path(r'../digikey/data')

class OAuth2Token:
    ''' OAuth2Token properties '''
    def __init__(self, token):
        self._token = token
        
    @property    
    def access_token(self):
        return self._token.get('access_token')
    
    @property
    def refresh_token(self):
        return self._token.get('refresh_token')
    
    @property
    def expires(self):
        return datetime.fromtimestamp(self._token.get('expires'), timezone.utc)
    
    @property
    def token_type(self):
        return self._token.get('token_type')
    
    @property
    def refresh_expires(self):
        return self._token.get('refresh_token_expires_in')
    
    def expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires
    
    def get_authorization(self) -> str:
        return self.token_type + ' ' + self.access_token
    
    def __repr__(self):
        return '<Token: expires={}>'.format(self.expires.astimezone().isoformat())

class TokenHandler:
    '''
    Handles Digi-Key OAuth Functions
    '''
    def __init__(self,
                 a_id: t.Optional[str] = None,
                 a_secret: t.Optional[str] = None,
                 a_username: t.Optional[str] = None,
                 a_password: t.Optional[str] = None,
                 a_callback: t.Optional[str] = None,
                 a_token_storage_path: t.Optional[str] = None,
                 version: int=1,
                 sandbox: bool=False):
        if version == 1:
            if sandbox:
                self.auth_url = AUTH_URL_V1_SB
                self.token_url = TOKEN_URL_V1_SB
            else:
                self.auth_url = AUTH_URL_V1_PROD
                self.token_url = TOKEN_URL_V1_PROD
        else:
            raise ValueError("Specify the correct Digi-Key API version (V1)")
        
        logger.debug(f'Using API V{version}')
        
        a_id = a_id or os.getenv('DIGIKEY_CLIENT_ID')
        a_secret = a_secret or os.getenv('DIGIKEY_CLIENT_SECRET')
        if not a_id or not a_secret:
            raise ValueError(
                'CLIENT ID and SECRET must be set. '
                'Set "DIGIKEY_CLIENT_ID" and "DIGIKEY_CLIENT_SECRET" '
                'as an environment variable, or pass your keys directly to the client.'
            )
        a_token_storage_path = a_token_storage_path or os.getenv('DIGIKEY_STORAGE_PATH')
        if not a_token_storage_path or not Path(a_token_storage_path).exists():
            raise ValueError(
                'STORAGE PATH must be set and must exist.'
                'Set "DIGIKEY_STORAGE_PATH" as an environment variable, '
                'or pass your keys directly to the client.'
            )
        a_username = a_username or os.getenv('DIGIKEY_USERNAME')
        a_password = a_password or os.getenv('DIGIKEY_PASSWORD')
        if not a_username or not a_password:
            raise ValueError(
                'DIGIKEY_USERNAME and DIGIKEY_PASSWORD credentials must be set. '
                'Set "DIGIKEY_USERNAME" and "DIGIKEY_PASSWORD" as an environment'
                ' variable, or pass your keys directly into the client.'
            )
        a_callback = a_callback or os.getenv('REDIRECT_URL')
        if not a_callback:
            raise ValueError(
                'REDIRECT_URL must be set and must be a valid redirect url. '
                'Set "REDIRECT_URL" as an environment variable, '
                'or pass your keys directly into the client.'
            )
        self._id = a_id
        self._secret = a_secret
        self._username = a_username
        self._password = a_password
        self._callback = a_callback
        self._storage_path = Path(a_token_storage_path)
        self._token_storage_path = self._storage_path.joinpath(TOKEN_STORAGE)
        # self._ca_cert = self._storage_path.joinpath(CA_CERT)
        
    def __build_authorization_url(self, redirect_uri):
        oauth = OAuth2Session(self._id, redirect_uri=redirect_uri)
        authorization_url, state = oauth.authorization_url(self.auth_url) 
        authorize_url = SelLogin('chrome').GET_code(authorization_url, self._username, self._password)
        return authorize_url

    def authorization_code(self, url):
        url = str(url)
        try:
            code = url.split('?code=')[1].split('&')[0]
        except IndexError:
            raise IndexError("Digi-Key did not return authorization code.")
        return code

    def __exchange_for_token(self, code) -> str:
        if code is None:
            raise TypeError("Unable to get code")
        post_data = {'code': code,
                'client_id': self._id,
                'client_secret': self._secret,
                'redirect_uri': self._callback,
                'grant_type': 'authorization_code'
               }
        try:
            access_response = requests.post(self.token_url, data=post_data, verify=False, allow_redirects=False, auth=(self._id, self._secret))
            access_response.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            raise DigikeyOauthException('Cannot request new token with auth code: {}'.format(error_message))
        if access_response.status_code != 200:
            return ("Access Failed: {}".format(access_response.status_code))
        token_json = access_response.json()
        # Creating an epoch timestamp from expires in, with 1 minute margin
        token_json['expires'] = int(token_json['expires_in']) + datetime.now(timezone.utc).timestamp() - 60
        return token_json

    def __refresh_token(self, refresh_token):
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 
                   'Accept': 'application/json'}
        post_data = {'client_id': self._id,
                     'client_secret': self._secret,
                     'refresh_token': refresh_token,
                     'grant_type': 'refresh_token'}
        error_message = None
        try:
            refresh_response = requests.post(self.token_url, data=post_data, headers=headers)
            error_message = refresh_response.json().get('error_description', None)
            refresh_response.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            raise DigikeyOauthException('Cannot request new token with refresh token: {}'.format(error_message))
        token_json = refresh_response.json()
        token_json['expires'] = int(token_json['expires_in']) + datetime.now(timezone.utc).timestamp() - 60
        return token_json

    def save(self, json_data):
        with open(self._token_storage_path, 'w') as f:
            json.dump(json_data, f, indent=4)
        logger.debug('Saved token to: {}'.format(self._token_storage_path))

    def get_access_token(self) -> OAuth2Token:
        # check if the token already exists in storage
        token_json = None
        try:
            with open(self._token_storage_path, 'r') as f:
                token_json = json.load(f)
        except (EnvironmentError, JSONDecodeError, TypeError):
            logger.warning("Token storage does not exist or is malformed, creating new.")

        token = None
        if token_json is not None:
            token = OAuth2Token(token_json)

        # Try to refresh the credentials with the stores and refresh token
        if token is not None and token.expired():
            try:
                token_json = self.__refresh_token(token.refresh_token)
                self.save(token_json)
            except DigikeyOauthException:
                logger.error('Failed to use refresh token, starting new authorization flow.')
                token_json = None

        # Obtain new credentials using the Oauth flow if no token stored or refresh fails
        if token_json is None:
            code_url = self.__build_authorization_url(self._callback)
            # print("Access URL:", code_url) # debug
            access_code = self.authorization_code(code_url)
            print("Access Code:", access_code)
            token_json = self.__exchange_for_token(access_code)
            self.save(token_json)
        return OAuth2Token(token_json)
                
                
                
            


