# sc2-bot-test
simple sc2 bot using voidray tactic

Getting Started
1. Install Starcraft 2 (system requirements)
a. It’s free (up to a point) and available for Windows and macOS
b. Linux users should be able to use Windows version with Wine. Headless Linux is also available.

2. Download and install latest Ladder 2019 Season 3 map pack (notice the zip password and instructions)
3. Install Python 3.7 if needed, preferably 64-bit
a. Python 3.6 is okay and 3.8 won’t work afaik
4. Clone the bot template and cd to its folder
5. Create a virtual environment for Python (exact commands may vary slightly)
a.
python3 -m venv .myvenv
b.
source ./myvenv/bin/activate
i.
this needs to be called with every new console window
6. Install python-sc2 library and other requirements (using the commands below)
a.
pip install -r requirements.txt
b.
pip install --upgrade --force-reinstall https://github.com/BurnySc2/python-sc2/archive/develop.zip
7. Run the example bot
a.
python3 run.py
8. If Starcraft 2 launches and it does not crash, you should be good to go!
