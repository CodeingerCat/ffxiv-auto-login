
import pyautogui
pyautogui.PAUSE = 0

from libs.Session import Session
from processes.core import init_core
from processes.login import init_login

from argparse import ArgumentParser
import json

import logging
import traceback
from libs.logging_util import configure_logger

### Argument Parsing ###
arg_psr = ArgumentParser()
arg_psr.add_argument('--fast_login', action='store_true', help="Continusly check for login instead of using hotkey")
arg_psr.add_argument('--log_level', type=str, default='INFO', help="Log Level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
args = arg_psr.parse_args()

try:
    ### Set up logging ###
    # Configure root logger
    configure_logger(logging.getLogger(), level_name=args.log_level)


    ### Load Configurations ###
    with open("../res/config.json") as config_file:
        config = json.load(config_file)


    ### Setup Base Session ###
    # Start up core processes
    session = Session()
    core_info = init_core(session)

    # Start up login processes
    login_info = init_login(session, config, core_info, args.fast_login)
    if(not args.fast_login):
        logging.info("Press Alt+Ctrl+F to start login process")


    ### Main loop ###
    try:
        session.start()
    except KeyboardInterrupt:
        logging.debug("[Exiting] keyboard interrupt")
        pass

# Capture critical exceptions to print with logger
except Exception as e:
    err_str:str = traceback.format_exc()
    err_str = err_str[:-1].replace('\n','\n\t')
    logging.critical("Unhandeld Exception Encountered\n\t" + err_str)
