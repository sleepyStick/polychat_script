from datetime import datetime, timedelta
import getpass
from starRez import starRezDB
from path_constants import *
from util import get_API_key, get_config, get_entry_id, get_resident_list

def main():
    config = get_config()
    email = config['email']
    community = config['community']

    #TODO make this autofill at some point
    #Resident Name & Entry ID
    res_name_list = get_resident_list()
    search_input = input("Search your resident by first or last name: ")
    while True:
        results = list(filter(lambda x: search_input in x['Name'], res_name_list))
        if len(results) == 1:
            entry_id = results[0]['EntryID']
            res_name = results[0]['Name']
            print(f"Resident Selected: {res_name}")
            break
        elif len(results) == 0:
            print("No results, try again")
            search_input = input("Resident Name: ")
            continue
        for i in range(len(results)):
            print(f"[{i}]:\t{results[i]['Name']}")
        print("Type the number of the resident you are enterring, or type another name")
        user_input = input("# or Resident Name: ")
        try:
            entry_id = results[int(user_input)]['EntryID']
            res_name = results[int(user_input)]['Name']
            break
        except:
            search_input = user_input
            continue



    #Date of the polychat
    while True:
        date_in = input("Date (leave blank for today) (MM/DD/YY): ")
        try:
            if date_in:
                date_sep = date_in.split("/")
                assert len(date_sep) == 3
                chat_date = datetime( int(date_sep[2]) + 2000,
                    int(date_sep[0]), 
                    int(date_sep[1]),
                    hour=12)
            else:
                chat_date = datetime.now()
        except:
            print("Invalid date. Follow the format MM/DD/YY")
            continue
        break

    #custom fields (LO's & description)
    custom_fields = get_custom_fields()

    #TODO make this dynamic and preferably switch over automatically
    term_session_id = 194

    #TODO make this only do first name unless you have conflicting first names
    chat_title = f"{res_name}-{datetime.today().strftime('%B')}-PC"

    password = getpass.getpass()
    API_key = get_API_key(password)

    starRez = starRezDB(email, API_key)

    chat_id = starRez.make_polychat(entry_id=entry_id,
        chat_begin=chat_date,
        chat_end=chat_date + timedelta(minutes=15),
        custom_fields=custom_fields,
        term_session_id=term_session_id,
        chat_title=chat_title,
        community=community)
    starRez.submit_polychat(chat_id)

def get_custom_fields():
    result = {}
    #Description
    while True:
        result['description'] = input("Description: ")
        if len(result['description']) > 0:
            break

    for LO in ['beTheChange', 'beWell', 'beSmart']:
        while True:
            try:
                result[LO] = input(LO+": ")
                result[LO] = int(result[LO]) if result[LO] else 0
            except:
                print("Please input an integer 0-3")
                continue
            if result[LO] >=0 and result[LO] <= 3:
                break
            else:
                print("Please input an integer 0-3")
    return result


if __name__ == "__main__":
    main()