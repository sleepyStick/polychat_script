import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import quote
from path_constants import *
import pyAesCrypt

mutable_tables = ['Program', 'ProgramEntry', 'ProgramCustomField']

class starRezDB:
    BASE_URL = "https://calpoly.starrezhousing.com/StarRezREST/services"

    def __init__(self, email, API_key):
        self.sess = requests.Session()
        self.sess.headers = {'Accept': 'application/json'}
        self.sess.auth = (email, API_key)

    # high level methds to create chats & such

    def make_polychat(self,
        entry_id=None,
        chat_begin=None,
        chat_end=None,
        custom_fields=None,
        term_session_id=None,
        chat_title=None,
        community=None):

        #load the template
        with open(TEMPLATE_PATH) as template_file:
            template_json = json.load(template_file)[0]
        template_json['Title'] = chat_title
        template_json['DateStart'] = chat_begin.isoformat()
        template_json['DateEnd'] = chat_end.isoformat()
        template_json['Community'] = community
        template_json['TermSessionID'] = term_session_id

        program_id = self.create_item("Program", template_json)['ProgramID']

        self.add_resident_to_chat(program_id, entry_id)

        self.add_custom_fields_to_chat(program_id, custom_fields)

        return program_id

    def add_resident_to_chat(self, program_id, entry_id):
        return self.create_item("ProgramEntry",
            params={
                "ProgramID": program_id,
                "EntryID": entry_id
            })['ProgramEntryID']

    def add_custom_fields_to_chat(self, program_id, cust_fields):
        custom_field_defs = {
        "description": 240,
        "beSmart": 401,
        "beWell": 402,
        "beTheChange": 403
        }

        cust_fields_from_id = {custom_field_defs[label]: val for label, val in cust_fields.items()}
        
        query = f'SELECT ProgramCustomFieldID, CustomFieldDefinitionID FROM ProgramCustomField WHERE ProgramID = "{program_id}"'
        custom_fields_SR = self.query(query)
        custom_fields_SR = list(filter(lambda x: (x['CustomFieldDefinitionID'] in custom_field_defs.values()), custom_fields_SR))
        tableName = "ProgramCustomField"
        for custom_field_SR in custom_fields_SR:
            field_id = custom_field_SR['ProgramCustomFieldID']
            field_def_id = custom_field_SR['CustomFieldDefinitionID']
            field_val = cust_fields_from_id[field_def_id]
            isInt = isinstance(cust_fields_from_id[field_def_id], int)
            self.update_item(tableName, field_id, params={"ValueInteger" if isInt else "ValueString": field_val})

        return [field['ProgramCustomFieldID'] for field in custom_fields_SR]


    def delete_polychat(self, chatID):
        query = f'SELECT ProgramEntryID FROM ProgramEntry WHERE ProgramID = {chatID}'
        entryIDs = [entry['ProgramEntryID'] for entry in self.query(query)]
        #delete all the program entrys (if you don't you get a 400 back when deleting the program)
        for entryID in entryIDs:
            self.delete_item("ProgramEntry", entryID)
        self.delete_item('Program', chatID)

    def get_polychat_residents(self, chatID):
        query = f"SELECT EntryID FROM ProgramEntry WHERE ProgramID = {chatID}"
        return [entry['EntryID'] for entry in self.query(query)]



    # Low Level Database access methods
    def query(self, query):
        response = self.sess.get(f"{self.BASE_URL}/query?q={quote(query)}")
        if not response.ok:
            raise Exception(f"Tried to query: {query}\nGot back {response.status_code}: {response.reason}")
        return response.json()

    def get_item(self, tableName, itemID):
        query = f'SELECT * FROM {tableName} WHERE {tableName}ID = {itemID}'
        return self.query(query)[0]

    def create_item(self, tableName, params={}):
        if not tableName in mutable_tables:
            raise Exception(f"Tried to mutate {tableName} which is not a mutable table")
        response = self.sess.get(f"{self.BASE_URL}/create/{tableName}", params=params)
        if not response.ok:
            raise Exception(f"Tried to create object in {tableName}\nGot back {response.status_code}: {response.reason}\nparams: {params}")
        return response.json()


    def update_item(self, tableName, itemID, params={}):
        if not tableName in mutable_tables:
            raise Exception(f"Tried to mutate {tableName} which is not a mutable table")
        response = self.sess.get(f"{self.BASE_URL}/update/{tableName}/{itemID}", params=params)
        if not response.ok:
            raise Exception(f"Tried to update: {itemID} in {tableName}\nGot back {response.status_code}: {response.reason}\nparams: {params}")


    def delete_item(self, tableName, itemID):
        #make sure we're deleting from okay tables
        if tableName not in mutable_tables:
            raise Exception(f"Tried to modify {tableName} which is not a mutable table")
        
        #make sure we're deleting an item that we created
        with open(CONFIG_PATH) as config:
            config_json = json.load(config)
        userID = config_json['SecurityID']
        if userID != self.get_owner(tableName, itemID):
                raise Exception(f"Tried to modify {itemID} in {tableName} which is not owned by you!")
        response = self.sess.get(f"{self.BASE_URL}/delete/{tableName}/{itemID}")
        if not response.ok:
            raise Exception(f"Tried to delete: {itemID} from {tableName}\nGot back {response.status_code}: {response.reason}")

    def get_owner(self, tableName, itemID):
        if tableName == 'ProgramCustomField':
            #special verification for these bad boys, since they don't have a secUserID themselves
            cust_field = self.get_item("ProgramCustomField", itemID)
            return self.get_item("Program", cust_field['ProgramID'])['AssignedTo_SecurityUserID']
        elif tableName in ['Program', 'ProgramEntry']:
            return self.get_item(tableName, itemID)['AssignedTo_SecurityUserID']

        else:
            raise Exception(f"{tableName} is not supported by get_owner. Should be one of: {mutable_tables}")






