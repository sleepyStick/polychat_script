import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote
import json
import pyAesCrypt
import os
from starRez import query_DB

API_auth = None
headers = None
def main():
    #get the users login information
    email = input("Please type your email here: ")
    API_key = input("Please paste your API key here: ")
    password = input("Please make a GOOD password: ")

    #encrypt the API key
    with open('temporary', 'w') as tempFile:
        tempFile.write(API_key)
    pyAesCrypt.encryptFile('temporary', 'config/key.aes', password)
    os.remove('temporary')

    #write all the other config information
    config_json = {}
    config_json['email'] = email
    #get their floor
    building_code = input("Building code (IE 172D): ").upper()
    floor = input("Floor: ")

    #get ready to get the their residents
    API_auth = HTTPBasicAuth(email, API_key)
    headers = {'Accept': 'application/json'}

    names = get_resident_names(building_code, floor)

    #get the security ID
    query = f'SELECT SecurityUserID FROM SecurityUser WHERE EmailAddress = "hevans03@calpoly.edu"'
    SecurityID = query_DB(query)[0]["SecurityUserID"]

    #Figure out the community
    

    #Write to config files

    config_json['SecurityID'] = SecurityID
    with open('config/config.json', 'w') as config_file:
        json.dump(config_json, config_file)
    
    #write resident names to a file
    with open('config/residentNames.json', 'w') as names_file:
        json.dump(names, names_file)

if __name__ == "__main__":
    main()

def get_resident_names(building_code, floor):
    #query selects the first and last names and the EntryID  from the Booking table 
    # where the roomspace matches user inputs and the booking is InRoom
    query = f'SELECT NameLast, NameFirst, EntryID FROM Booking JOIN Entry WHERE RoomSpace like "{building_code}-{floor}%" And EntryStatusEnum = "5" ORDER BY Entry.NameLast' 
    #request the data from the server
    return query_DB(query).json()

    