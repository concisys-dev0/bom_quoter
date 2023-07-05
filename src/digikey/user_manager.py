import json
import os
from utils import *
#json files
USER_STORAGE = 'digikey_user.json'
TOKEN_STORAGE = 'digikey_token.json'
#Production
AUTH_URL_V1_PROD = "https://api.digikey.com/v1/oauth2/authorize"
TOKEN_URL_V1_PROD = "https://api.digikey.com/v1/oauth2/token"
#Sandbox
AUTH_URL_V1_SB = "https://sandbox-api.digikey.com/v1/oauth2/authorize"
TOKEN_URL_V1_SB = "https://sandbox-api.digikey.com/v1/oauth2/token"

class DigikeyUser:
    ''' Digi-Key User properties for a single user '''
    def __init__(self, user_dictionary):
        self._user = user_dictionary # dictionary
    
    def decode_data(self, data_str):
        # check if the text is obfuscated
        if is_obfuscated(data_str) is True:
            data_str = decode_text(data_str)
        else:
            pass
        return data_str
        
    @property
    def user_id(self):
        self._user_id = self._user.get('user_id')
        return self._user_id
    
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
        \n ---------------------
        \nUserID: {self.user_id}
        \nEmail: {self.username}
        \nPassword: {self.password}
        \nClient ID: {self.client_id}
        \nClient Secret: {self.client_secret}
        '''
        return '{}'.format(user_display)
        
class UserManager:
    def __init__(self, user_id=None):
        pass
    
    def secure_data(self, data_str):
        # check if the text is obfuscated
        if is_obfuscated(data_str) is False:
            data_str = encode_text(data_str)
        else:
            pass
        return data_str
    
    def verify_user_file(self):
        with open(USER_STORAGE, 'r') as file:
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
        with open(USER_STORAGE, 'w') as writer:
            json.dump(secured_user_list, writer, indent=4, separators=(',',': '))
             
    def get_user(self, user_id=None):
        with open(USER_STORAGE, 'r') as file:
            try:
                user_list = json.load(file) # list of digikey users
            except JSONDecodeError:
                raise JSONDecodeError("Error with file")
            except FileNotFoundError:
                raise FileNotFoundError("File not found")
            except Exception as e:
                raise e
        if len(user_list) > 0:
            if user_id is None:
                first_user = user_list[0]
                current_user = DigikeyUser(first_user) # take the first if user_id is None
            elif isinstance(user_id, int):
                u_index = user_id
                current_user = DigikeyUser(u_index)
            else:
                for user in user_list:
                    if user['user_id'] == user_id:
                        current_user = DigikeyUser(user)
        else:
            return "User storage is empty"
        return current_user
    
    def create_new_user(self):
        print("***WARNING: PLEASE KEEP DIGI-KEY LOGIN INFO PRIVATE.\nPASSWORD, CLIENT ID, AND CLIENT SECRET WILL BE HIDDEN.***")
        user_id = str(input("Enter your name: "))
        redirect_uri = str(input("Enter your callback url: "))
        username = str(input("Enter Digi-Key email: "))
        password = str(input("Enter password: "))
        client_id = str(input("Enter client ID: "))
        client_secret = str(input("Enter client secret: "))
        
        user_data = {
            'user_id': user_id,
            'redirect_uri': redirect_uri,
            'username': username,
            'password': self.secure_data(password),
            'client_id': self.secure_data(client_id),
            'client_secret': self.secure_data(client_secret)
        }
        self.append_new_user(user_data, USER_STORAGE)
    
    def append_new_user(self, user_auth, user_file):
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
                    print("json error")
                    with open(user_file, 'w') as newjson:
                        users_data = [user_auth]
                        json.dump(users_data, newjson, indent=4, separators=(',',': '))
        return "New Digi-Key user added"
    
    
        
    # def retry_dk_user(self, user_data, authorize_type='PROD'):
    #     with open(USER_STORAGE, 'r') as file:
    #         u_list = json.load(file)
    #         u_list.pop(u_list.index(user_data))
    #     if len(u_list) == 0:
    #         return("No users available")
    #     for i in range(len(u_list)):
    #         n_user = u_list[i] # get the next user in u_list
    #         if authorize_type is 'PROD':
    #             authorize_url = AUTH_URL_V1_PROD
    #             token_url = TOKEN_URL_V1_PROD
    #         elif authorize_type is 'SB':
    #             authorize_url = AUTH_URL_V1_SB
    #             token_url = TOKEN_URL_V1_SB
            
        
        
        