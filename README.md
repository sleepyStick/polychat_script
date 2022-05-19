# PolyChat Script
This script is designed to be used by Cal Poly Resident Advisors to assist in the creation of polychats. This script interfaces with the StarRez API to create Polychats, and autofill all of the fields (community, term session, Program Type) that rarely if ever change. It's a command line script that runs on python.

## Setup
1. Download this repo, either using `git clone` or download a zip file that I will make at some point.
2. If you haven't already, install a reasonably up to date version of Python. 
    - Download python from the following link (you want the 64-bit Windows or MacOS version): [Download](https://www.python.org/downloads/release/python-3913/). It is near the bottom of the page
    - Follow the steps of the installer (all the defaults are fine)
    - *NOTE*: While MacOS does come preinstalled with python, it is python2 which is older than dirt at this point. Install python3.
3. Open a terminal in this folder and run `pip3 install -r requirements.txt`
4. Run  `python3 setup.py`, and answer the prompts
    - Cal Poly email: Pretty self explanatory. This will be used to log into the StarRez API so yes, it does need to be your Cal Poly email.
    - API Key:
        - Log into StarRez and click the person icon in the top left corner.
        - Click "Account"
        - Scroll down to the "Web Security Tokens" and click the plus icon
        - *IMPORTANT*: Copy the token name, and paste it into the script, but DON'T press enter yet
        - Give the token a name (it doesn't really matter what), and click "Save Token"
        - Press enter on the script. If the Token hasn't been saved yet, the script will reject it, so be sure to press enter after you save the token
    - password: API keys are very sensitive pieces of data. (With your API Key anybody can do everything you can do in StarRez), so the API Keys are encrypted with AES-256 encryption. Please use good passwords. I know it's annoying, but it is important.
    - Community. Input your community, at the moment there is no input validation on this, so be sure to get it right. If you live in yakʔitʸutʸu, you can abbreviate it to ytt <1 or 2>. Use a space between the community and the number.
    - Building code: this is the (typically) 3 digit number followed by a letter that designates your building. Hopefully in the future you can just input this and I can figure out your community from this value.
    - floor number: What you think it is. This and the building code are used so you can search a list of just your residents.
5. You should be good! Run `python3 polychat.py` and start making polychats 10x faster that StarRez lets you.

## TODO:
- Error Checking
    * ~~When requests return 400 errors~~
    * ~~Bad user input~~
- A way to search resident names
- Make more things configurable on setup (~~community~~, current term)
- change terms (Fall, Spring, Winter) automatically
- 
