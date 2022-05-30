from datetime import datetime, timedelta
import argparse
import getpass
from starRez import starRezDB
from util import get_API_key, get_config, get_resident_list
from typing import Optional


def get_name(res_name_list,
             search_input: Optional[str] = None) -> tuple[str, int]:
    if not search_input:
        search_input = input("Search your resident by first or last name: ")
    while True:
        results = list(filter(lambda x: search_input in x['Name'],
                              res_name_list))
        if len(results) == 1:
            entry_id = results[0]['EntryID']
            res_name = results[0]['Name']
            print(f"Resident Selected: {res_name}")
            return entry_id, res_name
        elif len(results) == 0:
            print("No results, try again")
            search_input = input("Resident Name: ")
            continue
        for i in range(len(results)):
            print(f"[{i}]:\t{results[i]['Name']}")
        print("Type the number of the resident you are enterring, "
              "or type another name")
        user_input = input("# or Resident Name: ")
        try:
            entry_id = results[int(user_input)]['EntryID']
            res_name = results[int(user_input)]['Name']
            return entry_id, res_name
        except:
            search_input = user_input
            continue


def get_date() -> datetime:
    while True:
        date_in = input("Date (leave blank for today) (MM/DD/YY): ")
        try:
            if date_in:
                date_sep = date_in.split("/")
                assert len(date_sep) == 3
                chat_date = datetime(int(date_sep[2]) + 2000,
                                     int(date_sep[0]),
                                     int(date_sep[1]),
                                     hour=12)
            else:
                chat_date = datetime.now()
            return chat_date
        except:
            print("Invalid date. Follow the format MM/DD/YY")
            continue


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Process polychat script flags')
    parser.add_argument('-n', '--name', type=str,
                        dest='name',
                        help='resident name')
    parser.add_argument('-d', '--description', type=str,
                        dest='desc',
                        help='polychat description')
    parser.add_argument('-c', '--beTheChange', type=str, default="0",
                        dest='change',
                        help='be the change')
    parser.add_argument('-w', '--beWell', type=str, default="0",
                        dest='well',
                        help='be well')
    parser.add_argument('-s', '--beSmart', type=str, default="0",
                        dest='smart',
                        help='be smart')
    parser.add_argument('-p', '--password', type=str, default="",
                        dest='password',
                        help='star res api password')
    return parser.parse_args()


def main():
    args = parse_args()
    config = get_config()
    email = config['email']
    community = config['community']

    # TODO make this autofill at some point
    # Resident Name & Entry ID
    res_name_list = get_resident_list()
    entry_id, res_name = get_name(res_name_list, args.name)

    # Date of the polychat
    # chat_date = get_date()
    chat_date = datetime.now()

    # custom fields (LO's & description)
    custom_fields = get_custom_fields(
        args.desc, args.change, args.well, args.smart)

    # TODO make this dynamic and preferably switch over automatically
    term_session_id = 194

    # TODO make this only do first name unless you have conflicting first names
    chat_title = f"{res_name}-{datetime.today().strftime('%B')}-PC"

    password = args.password if args.password else getpass.getpass()
    API_key = get_API_key(password)

    starRez = starRezDB(email, API_key)

    chat_id = starRez.make_polychat(
        entry_id=entry_id,
        chat_begin=chat_date,
        chat_end=chat_date + timedelta(minutes=15),
        custom_fields=custom_fields,
        term_session_id=term_session_id,
        chat_title=chat_title,
        community=community)
    starRez.submit_polychat(chat_id)


def get_custom_fields(desc, change, well, smart):
    result = {}
    # Description
    while True:
        result['description'] = desc if desc else input("Description: ")
        if len(result['description']) > 0:
            break
    temp = [change, well, smart]
    for i, LO in enumerate(['beTheChange', 'beWell', 'beSmart']):
        while True:
            try:
                result[LO] = temp[i] if temp[i] else input(LO+": ")
                result[LO] = int(result[LO]) if result[LO] else 0
            except:
                print("Please input an integer 0-3")
                continue
            if result[LO] >= 0 and result[LO] <= 3:
                break
            else:
                print("Please input an integer 0-3")
    return result


if __name__ == "__main__":
    main()
