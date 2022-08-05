# FFXIV Atuto Login
## Description
The purpos of this project is to make opening FFXIV less anoying when opening the client.
Currently the only qulity of life improvment it dose is enter your password into the launcher then start the game for you.

*NOTE: This project only works on windows since it used the pypiwin32 package*

## How to Setup and Run
*NOTE: This project is not paticularly user frendly yet so some experience with cmd promts is recomened*

1. **Python** 
    This is a Python project so if you havent already go download [Python](https://www.python.org/).
2. **Download**
    Download this project.

3. **Virtual Enviroment**
    Run *update_venv.bat* witch should create a virtual enviroment and download needed Python packages.
4. **Configurations**
    This project stores your password for logging in, in a configuration file that needs to be set up.
    To set up this file src/init_config.py will nead to be run within the Virtual Enviroment with the FFXIV password as a argument to it.

    To do this you will nead to open up a command terminal and ether activate the Venv yourself of run *start_vent.bat* to activate it. Once the Venv is active run *"python src/init_config.py -pwd [Password]"* and the config file should be created. To update the password if need simpy use this same command with the new password. 

5. **Run FFXIV Auto**
    Now you can run *start_ffxiv_auto.bat*, wich will open up FFXIV Auto and the FFXIV launcher.  If both open up you just have to make shure FFXIV Launcher is fully visable on your main monitor and it will log you right in.

    *NOTE: I personlay have hooked up a shortcut on my desktop to start_ffxiv_auto for convinience*
