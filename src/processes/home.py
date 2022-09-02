
import logging
from libs.Session import Session, ProcessInfo
import win32.lib.win32con as win32con

from libs.save_desc import SaveDesc
from processes.core import Core_Info

import PySimpleGUI as sg
from processes.crafting import open_crafting_menue
from processes.login import open_password_menue
from processes.testbench import open_testbench_window

class ButtonCallback:
    def __init__(self, func, *args) -> None:
        self.func = func
        self.args = args

class Home_Info(ProcessInfo):
    save_desc = SaveDesc("Home", ["window_location"])

    def __init__(self):
        self.window:sg.Window = None
        self.window_location = [0,0]
        self._window_buttons = []

def init_home(session:Session, info:Home_Info):
     # Start up inital instance of main menue
    open_home_window(session, info)
    session.add_hotkey(
        ord('M'), win32con.MOD_CONTROL | win32con.MOD_ALT, 
        open_home_window, info
    )

    return info

def open_home_window(session:Session, info:Home_Info):
    # Check if main menue already exsists
    if(info.window != None): return

    # Create main menue window
    info.window = sg.Window(title="Auto FFXIV", layout=[
        [sg.Text("Main Menue", font="Helvitica 11 bold")],
        [sg.Button("Edit Password", metadata=ButtonCallback(open_password_menue, session, session.get_info("Login")) )],
        [sg.Button("Auto Crafting", metadata=ButtonCallback(open_crafting_menue, session, session.get_info("Crafting")) )],
        [sg.Button("Testbench", metadata=ButtonCallback(open_testbench_window, session, session.get_info("Testbench")) )]
    ], margins=(100,None), location=info.window_location)
    info._window_buttons = ["Edit Password", "Auto Crafting", "Testbench"]

    # Init main_menue task
    session.add_task("home_menue_task", home_menue_task, info)

def home_menue_task(session:Session, info:Home_Info):
    event, values = info.window.read(timeout=0)

    if(event == sg.WINDOW_CLOSED):
        logging.info("Home menue closed, to open again you can press [Crtl+Alt+M]")
        info.window.close()
        info.window = None
        return False
    
    info.window_location = info.window.CurrentLocation()

    if(event == sg.TIMEOUT_EVENT):
        pass
    elif(event in info._window_buttons):
        btn_cb = info.window[event].metadata
        btn_cb.func(*(btn_cb.args))
    else:
        logging.warn(f"Core Menue -- Unrecognised menue event '{event}'.")

    return True

