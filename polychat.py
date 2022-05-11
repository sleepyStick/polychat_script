import json
from datetime import datetime, timedelta
import pyAesCrypt
import os
import requests
from requests.auth import HTTPBasicAuth
import getpass
from urllib.parse import quote

TEMPLATE_PATH = "config/template.json"
CONFIG_PATH = "config/config.json"
RESIDENTS_PATH = "config/residentNames.json"
KEY_PATH = "config/key.aes"

HTTP_headers = {"Accept": "application/json"}


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

    #load the template
    with open(TEMPLATE_PATH) as template_file:
       template_json = json.load(template_file)[0]
    template_json['Title'] = chat_title
    template_json['DateStart'] = chat_date.isoformat()
    template_json['DateEnd'] = (chat_date + timedelta(minutes=15)).isoformat()

    program_id = upload_chat(template_json, email, API_key)

    upload_resident(program_id, entry_id, email, API_key)

    upload_custom_fields(program_id, custom_fields, email, API_key)


def get_entry_id(res_name):
    with open(RESIDENTS_PATH) as residents_file:
        residents_json = json.load(residents_file)
    
    #TODO make it store the residents like this in the first place
    #create a dictionary that is actually useful
    residents_dict = {}
    for resident in residents_json:
        residents_dict[f"{resident['NameFirst']} {resident['NameLast']}"] = resident['EntryID']
    
    return residents_dict[res_name]

def get_config():
    with open(CONFIG_PATH) as config_file:
        config_json = json.load(config_file)
    return config_json

def get_API_key(password):
    pyAesCrypt.decryptFile(KEY_PATH, 'config/key', password)
    with open('config/key') as key_file:
        API_key = key_file.read()
    os.remove('config/key')
    return API_key

def upload_chat(chat_json, RA_email, API_Key):
    API_Auth = HTTPBasicAuth(RA_email, API_Key)
    create_url = get_create_url('Program')
    programID = requests.get(create_url,
        headers=HTTP_headers,
        params=chat_json,
        auth=API_Auth).json()['ProgramID']
    return programID

def upload_resident(program_id, entry_id, RA_email, API_Key):
    API_Auth = HTTPBasicAuth(RA_email, API_Key)
    create_url = get_create_url('ProgramEntry')
    program_entry_id = requests.get(create_url,
        headers=HTTP_headers,
        params={
            'ProgramID': program_id,
            'EntryID': entry_id
        },
        auth=API_Auth
        ).json()['ProgramEntryID']
    return program_entry_id

def upload_custom_fields(program_id, cust_fields, RA_email, API_Key):
    custom_field_defs = {
        "description": 240,
        "beSmart": 401,
        "beWell": 402,
        "beTheChange": 403
    }

    cust_fields_from_id = {custom_field_defs[label]: val for label, val in cust_fields.items()}
    API_Auth = HTTPBasicAuth(RA_email, API_Key)
    
    query = f'SELECT ProgramCustomFieldID, CustomFieldDefinitionID FROM ProgramCustomField WHERE ProgramID = "{program_id}"'
    query_url = get_query_url(query)
    custom_fields_SR = requests.get(query_url,
        headers=HTTP_headers,
        auth=API_Auth).json()
    custom_fields_SR = list(filter(lambda x: (x['CustomFieldDefinitionID'] in custom_field_defs.values()), custom_fields_SR))
    tableName = "ProgramCustomField"
    for custom_field_SR in custom_fields_SR:
        field_id = custom_field_SR['ProgramCustomFieldID']
        field_def_id = custom_field_SR['CustomFieldDefinitionID']
        field_val = cust_fields_from_id[field_def_id]
        isInt = isinstance(cust_fields_from_id[field_def_id], int)
        update_url = get_update_url(tableName, field_id)
        requests.get(update_url,
            headers=HTTP_headers,
            auth=API_Auth,
            params={
                "ValueInteger" if isInt else "ValueString": field_val
            })

    return [field['ProgramCustomFieldID'] for field in custom_fields_SR]

def get_create_url(tableName):
    return f"https://calpoly.starrezhousing.com/StarRezREST/services/create/{tableName}"

def get_update_url(tableName, itemID):
    return f"https://calpoly.starrezhousing.com/StarRezREST/services/update/{tableName}/{itemID}"

def get_query_url(query):
    return f'https://calpoly.starrezhousing.com/StarRezREST/services/query?q={quote(query)}'




if __name__ == "__main__":
    main()