from path_constants import *
import json
import pyAesCrypt
import os

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