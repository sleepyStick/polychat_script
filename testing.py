from zipapp import get_interpreter
from starRez import starRezDB
from util import get_API_key
from datetime import datetime, timedelta
from getpass import getpass

def test_basic_chat():
    email = "hevans03@calpoly.edu"
    args = {
        "entry_id": 126174,
        "chat_begin": datetime.now(),
        "chat_end": datetime.now() + timedelta(minutes=15),
        "custom_fields": {
            "description": "abcdefghijklmnopqrstuvwxyz",
            "beWell": 1,
            "beTheChange": 2,
            "beSmart": 3
        },
        "term_session_id": 194,
        "chat_title": "Testing chat",
        "community": "yakʔitʸutʸu 2"
    }

    API_Key = get_API_key(getpass())
    starRez = starRezDB(email, API_Key)
    print("creating chat")
    program_id = starRez.make_polychat(**args)
    print(f"made chat {program_id}!")

    try:
        chat = starRez.get_item("Program", program_id)
        resident_ids = starRez.get_polychat_residents(program_id)

        assert len(resident_ids) == 1
        assert resident_ids[0] == args['entry_id']

        assert chat["DateStart"] == datetime.now().replace(second=0, microsecond=0).isoformat()
        assert chat["DateEnd"] == (datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=15)).isoformat()
        assert chat["Be_the_Change_LO"] == args['custom_fields']['beTheChange']
        assert chat["Be_Well_LO"] == args['custom_fields']['beWell']
        assert chat["Be_Smart_LO"] == args['custom_fields']['beSmart']
        assert chat["Title"] == args['chat_title']
        assert chat["Community"] == args['community']
        assert chat["TermSessionID"] == 194

    except Exception as e:
        print(f"Something didn't work!: {e}")
    else: print("Chat passed all tests!")

    #Cleanup
    starRez.delete_polychat(program_id)
    print("Deleted chat")

if __name__ == "__main__":
    test_basic_chat()