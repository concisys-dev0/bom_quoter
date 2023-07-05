import json
import os
from pathlib import Path
from datetime import datetime, timezone

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

BASE_DIR = os.path.dirname(os.path.abspath(r'D:\\bom_quoter\\src\\digikey\\config.py'))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

AUTH_URL_V1_PROD = "https://api.digikey.com/v1/oauth2/authorize"
TOKEN_URL_V1_PROD = "https://api.digikey.com/v1/oauth2/token"
AUTH_URL_V1_SB = "https://sandbox-api.digikey.com/v1/oauth2/authorize"
TOKEN_URL_V1_SB = "https://sandbox-api.digikey.com/v1/oauth2/token"

USER_STORAGE = 'digikey_user.json'
TOKEN_STORAGE = 'digikey_token.json'

logger = logging.getLogger(__name__)

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
    
