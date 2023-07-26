import logging
import os
import re
import typing as t
import requests
from exceptions import DigikeyError
from oauth2 import TokenHandler
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.digikey.com/Search/v3"

class DigikeyClient(object):
    """
    Client object for Digikey API
    Visit https://developer.digikey.com/ to get an app key and secret, then set it as
    an environment variable or pass the key directly to this constructor.
    """
    
    def __init__(self,
                 a_id: t.Optional[str] = None,
                 a_secret: t.Optional[str] = None,
                 a_token_storage_path: t.Optional[str] = None,
                 base_url: t.Optional[str] = DEFAULT_BASE_URL) -> None:
        a_id = a_id or os.getenv('DIGIKEY_CLIENT_ID')
        a_secret = a_secret or os.getenv('DIGIKEY_CLIENT_SECRET')
        if not a_id or not a_secret:
            raise ValueError(
                'CLIENT ID and SECRET must be set. '
                'Set "DIGIKEY_CLIENT_ID" and "DIGIKEY_CLIENT_SECRET" '
                'as an environment variable, or pass your keys directly to the client.')
        a_token_storage_path = a_token_storage_path or os.getenv('DIGIKEY_STORAGE_PATH')
        if not a_token_storage_path or not Path(a_token_storage_path).exists():
            raise ValueError(
                'STORAGE PATH must be set and must exist.'
                'Set "DIGIKEY_STORAGE_PATH" as an environment variable, '
                'or pass your keys directly to the client.')
        self._id = a_id
        self._secret = a_secret
        self._token_storage_path = Path(a_token_storage_path).joinpath('token_storage.json')
        self.base_url = base_url
        self.oauth2 = TokenHandler().get_access_token()
    
    @property
    def client_key_param(self) -> t.Dict[str, str]:
        return {'clientid': self._id,
                'clientsecret': self._secret}
    
    @retry
    def _request(self,
                 path: str,
                 data: t.Dict[str, t.Any]=None,
                ) -> t.Any:
        headers = {'x-ibm-client-id': self._id,
                   'authorization': self.oauth2.get_authorization()}
        response = requests.post('%s%s' % (self.base_url, path), json=data, headers=headers)
        rate_limit = re.split('[,;]+', response.headers['x-ratelimit-limit'])[1]
        rate_limit_rem = re.split('[,;]+', response.headers['x-ratelimit-remaining'])[1]
        logger.debug('Requested Digikey URI: {} [{}/{}]'.format(response.url, rate_limit_rem, rate_limit))
        response.raise_for_status()
        return response.json()
    
    # def search(self,
    #            query: str, # maps to 'keyword' param in DigiKeyAPI
    #            start: int=0,
    #            limit: int=10,
    #           ) -> dict:
    #     """
    #     Search for part, using fields and filter options than 'match'.
    #     This calls the /parts/search endpoint of the API
    #     Params:
    #         query(str): free-form keyword query
    #         start(int): orginal position of the first result
    #         limit(int): maximum number of results to return
    #     Kwargs:
    #     Returns:
    #         dict. (Modules.PartsSearchResponse)
    #     """
    #     data = {
    #         'keywords': query,
    #         'search_options': None,
    #         'record_count': limit,
    #         'record_start_pos': start,
    #         'filters': None,
    #         'sort': None,
    #         'requested_quantity': 1}

                  
        