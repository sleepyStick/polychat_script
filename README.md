# PolyChat Script
This script is designed to be used by Cal Poly Resident Advisors to assist in the creation of polychats. This script interfaces with the StarRez API to create Polychats, and autofill all of the fields (community, term session, Program Type) that rarely if ever change. It's a command line script that runs on python.

## Setup
1. Download this repo, either using `git clone` or download a zip file that I will make at some point.
2. If you haven't already, install a reasonably up to date version of Python. 
    - Writing documentation for MacOS and Windows for this process is something of a pain, so I'm just gonna say google "How to install Python3 on [Insert your OS of choice here]"
3. Open a terminal in this repository and run `pip3 install -r requirements.txt`
4. Run  `python3 setup.py`, and answer the prompts
5. You should be good! Run `python3 polychat.py` and start making polychats 10x faster that StarRez lets you.

## TODO:
- Error Checking
    * ~~When requests return 400 errors~~
    * ~~Bad user input~~
- A way to search resident names
- Make more things configurable on setup (community, current term)
- change terms (Fall, Spring, Winter) automatically
- 
