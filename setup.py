
import json
from starRez import starRezDB
from util import write_API_key
from getpass import getpass

API_auth = None
headers = None
def main():
    #get the users login information
    while True:
        email = input("Please type your calpoly email here: ")
        print("To paste in command line, use either Ctr-Shift-V or right click depending on your OS")
        API_key = input("Please paste your API key here: ")
        #make sure these are valid by creating starRezDB object
        try:
            starRez = starRezDB(email, API_key)
        except:
            print("invalid email/API key combo. Try again")
            continue
        break

    print("Make a good password. It won't appear as you are typing it. This is normal.")
    password = getpass()
    community = input("List your community here (IE PCV 2) (If you live in yakʔitʸutʸu you can just type ytt1 or ytt2): ")
    community = community.replace(" ", "").replace("ytt", "yakʔitʸutʸu ")

    #encrypt the API key
    write_API_key(API_key, password)

    #write all the other config information
    config_json = {}
    config_json['email'] = email
    config_json['community'] = community
    #get their floor
    building_code = input("Building code (IE 172D): ").upper()
    floor = input("Floor: ")

    names = get_resident_names(starRez, building_code, floor)

    #get the security ID
    query = f'SELECT SecurityUserID FROM SecurityUser WHERE EmailAddress = "{email}"'
    try:
        SecurityID = starRez.query(query)[0]['SecurityUserID']
    except:
        raise Exception("Error when retrieving security user id. check you email address, and API key are correct")

    #Write to config files
    config_json['SecurityID'] = SecurityID
    with open('config/config.json', 'w') as config_file:
        json.dump(config_json, config_file)
    
    #write resident names to a file
    with open('config/residentNames.json', 'w') as names_file:
        json.dump(names, names_file)

def get_resident_names(starRez, building_code, floor):
    #query selects the first and last names and the EntryID  from the Booking table 
    # where the roomspace matches user inputs and the booking is InRoom
    query = f'SELECT NameLast, NameFirst, EntryID FROM Booking JOIN Entry WHERE RoomSpace like "{building_code}-{floor}%" And EntryStatusEnum = "5" ORDER BY Entry.NameLast' 
    #request the data from the server
    return starRez.query(query)

if __name__ == "__main__":
    main()

    