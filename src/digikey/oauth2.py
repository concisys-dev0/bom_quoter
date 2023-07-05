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
from datetime import dateatime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open_new
import typing as t
import ssl

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)
from user_manager import *
import digikey_driver as dk_driver
from utils import *

# files
CA_CERT = 'digikey-api.pem'
USER_STORAGE = 'digikey_user.json'
TOKEN_STORAGE = 'digikey_token.json'
#Production
AUTH_URL_V1_PROD = "https://api.digikey.com/v1/oauth2/authorize"
TOKEN_URL_V1_PROD = "https://api.digikey.com/v1/oauth2/token"
#Sandbox
AUTH_URL_V1_SB = "https://sandbox-api.digikey.com/v1/oauth2/authorize"
TOKEN_URL_V1_SB = "https://sandbox-api.digikey.com/v1/oauth2/token"


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
        self._code = None
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
        a_username = a_username or os.getenv('DKUSERNAME')
        a_password = a_password or os.getenv('DKPASSWORD')
        if not a_username or not a_password:
            raise ValueError(
                'DKUSERNAME and DKPASSWORD credentials myst be set. '
                'Set "DKUSERNAME" and "DKPASSWORD" as an environment'
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
            authorization_url, satte = oauth.authorization_url(self.auth_url)
            access_url = user_login(authorization_url, self._username, self._password)
            return access_url
        
        @property
        def authorization_code(self):
            return self._code
        
        @authorization_code.setter
        def authorization_code(self, value):
            try:
                self._code = value.split('?code=')[1].split('&')[0]
            except IndexError:
                raise IndexError("Digi-Key did not return authorization code.")
        
        def __exchange_for_token(self) -> str:
            if self._code is None:
                raise TypeError("Unable to get code")
            post_data = {'code': self._code,
                    'client_id': self._id,
                    'client_secret': self._secret,
                    'redirect_uri': self.redirect_uri,
                    'grant_type': 'authorization_code'
                   }
            access_response = requests.post(self.token_url, data=post_data, verify=False, allow_redirects=False, auth(self._id, self._secret))
            print(access_response.text)
            if access_response.status_code != 200:
                return ("Access Failed")
            tokens = access_token_reponse.json()
            access_token = write_digikey_token(tokens)
        
        def save(self, json_data):
            with open(self._token_storage_path, 'w') as f:
                json.dump(json_data, f, indent=4)
                logger.debug('Saved token to: {}'.format(self._token_storage_path)
            


