import json
import pyAesCrypt
import os
import requests
from urllib.parse import quote


def main():
    #get the email from the config file
    with open('config/config.json') as config_file:
        config_json = json.load(config_file)
    email = config_json['email']

    #get the API key
    password = input('Password: ')
    pyAesCrypt.decryptFile('config/key.aes', 'config/key', password)
    with open('config/key') as key_file:
        API_key = key_file.read()
    os.remove('config/key')

    #send the actual request
    API_auth = requests.auth.HTTPBasicAuth(email, API_key)
    headers = {'Accept': 'application/json'}
    query = f'SELECT NameLast, NameFirst FROM Booking JOIN Entry WHERE RoomSpace like "172D-2%" And EntryStatusEnum = "5" ORDER BY Entry.NameLast'
    response = requests.get(f'https://calpoly.starrezhousing.com/StarRezREST/services/query?q={quote(query)} / GET', 
    headers=headers,
    auth=API_auth).json()

    print(response)




    

if __name__ == "__main__":
    main()