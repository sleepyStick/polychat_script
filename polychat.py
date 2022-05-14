import json
from datetime import datetime, timedelta
import pyAesCrypt
import os
import requests
from requests.auth import HTTPBasicAuth
import getpass
from urllib.parse import quote
from starRez import make_polychat
from path_constants import *
from util import get_API_key, get_config, get_entry_id

def main():
    config = get_config()
    email = config['email']

    #TODO make this autofill at some point
    #Resident Name & Entry ID
    res_name = input("Resident Name: ")
    entry_id = get_entry_id(res_name)

    #Date of the polychat
    date_in = input("Date (leave blank for today) (MM/DD/YY): ")
    if date_in:
        date_sep = date_in.split("/")
        chat_date = datetime( int(date_sep[2]) + 2000,
            int(date_sep[0]), 
            int(date_sep[1]),
            hour=12)
    else:
        chat_date = datetime.now()

    #custom fields (LE's & description)
    custom_fields = {}
    #Description of the polychat
    custom_fields['description']= input("Description: ")

    custom_fields['beSmart'] = input("Be smart: ")
    custom_fields['beSmart'] = int(custom_fields['beSmart']) if custom_fields['beSmart'] else 0
    custom_fields['beTheChange'] = input("Be the change: ")
    custom_fields['beTheChange'] = int(custom_fields['beTheChange']) if custom_fields['beTheChange'] else 0
    custom_fields['beWell'] = input("Be well: ")
    custom_fields['beWell'] = int(custom_fields['beWell']) if custom_fields['beWell'] else 0

    #TODO make this dynamic and preferably switch over automatically
    term_session_id = 194

    #TODO make this only do first name unless you have conflicting first names
    chat_title = f"{res_name}-Spring-Polychat"

    #TODO make this configurable
    community = "yakʔitʸutʸu 2"

    password = getpass.getpass()
    API_key = get_API_key(password)

    make_polychat(email=email,
        entry_id=entry_id,
        chat_begin=chat_date,
        chat_end=chat_date + timedelta(minutes=15),
        custom_fields=custom_fields,
        term_session_id=194, #add this to the config file at some point
        chat_title=f"{res_name}-{datetime.today().strftime('%B')}-PC",
        API_Key=API_key,
        RA_email=email,
        community=community)


if __name__ == "__main__":
    main()