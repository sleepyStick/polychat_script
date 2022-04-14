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
    #for getting all residents on a given floor
    #query = f'SELECT NameLast, NameFirst FROM Booking JOIN Entry WHERE RoomSpace like "172D-2%" And EntryStatusEnum = "5" ORDER BY Entry.NameLast'
    secID = 898
    query = f'SELECT Title, EntryID, CreatedBy_SecurityUserID FROM Program JOIN ProgramEntry WHERE Community = "yakʔitʸutʸu 2" And DateCreated > "2022-03-01T00:00:00.001-08:00" And CreatedBy_SecurityUserID = "{secID}" ORDER BY Program.DateCreated'
    response = requests.get(f'https://calpoly.starrezhousing.com/StarRezREST/services/query?q={quote(query)} / GET', 
    headers=headers,
    auth=API_auth).json()
    with open('outfile.json', 'w') as outfile:
        json.dump(response, outfile)

    print(response)




    

if __name__ == "__main__":
    main()