
import json
from argparse import ArgumentParser

from libs.Session import Process, Session
from processes.core import init_core, Core_Info
from processes.login import init_login, Login_Info
from processes.crafting import init_crafting, Crafting_Info
from processes.testbench import init_testbench, Testbench_Info
from processes.home import Home_Info, init_home

import pyautogui
import traceback
import logging
from libs.logging_util import configure_logger

### Import option settings ###
pyautogui.PAUSE = 0

### Argument Parsing ###
arg_psr = ArgumentParser()
arg_psr.add_argument('--fast_login', action='store_true', help="Continusly check for login instead of using hotkey")
arg_psr.add_argument('--log_level', type=str, default='INFO', help="Log Level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
args = arg_psr.parse_args()

def cleanup():
    core_info._tracking_thread.running = False

try:
    ### Set up logging ###
    # Root Logger
    configure_logger(logging.getLogger(), level_name=args.log_level)

    ### Setup Base Session ###
    session = Session()
    core_info = Core_Info()
    session.add_process(Process("Core", init_core, core_info))
    session.add_process(Process("Home", init_home, Home_Info()))
    session.add_process(Process("Login", init_login, Login_Info(fast_login=args.fast_login)))
    session.add_process(Process("Crafting", init_crafting, Crafting_Info()))
    session.add_process(Process("Testbench", init_testbench,  Testbench_Info()))

    ### Main loop ###
    try:
        session.start(cleanup)
    except KeyboardInterrupt:
        logging.debug("[Exiting] keyboard interrupt")
        
        pass
    session.cleanup()

# Capture critical exceptions to print with logger
except Exception as e:
    err_str:str = traceback.format_exc()
    err_str = err_str[:-1].replace('\n','\n\t')
    logging.critical("Unhandeld Exception Encountered\n\t" + err_str)

# Close Extra Threads (if still open)
core_info._tracking_thread.running = False
