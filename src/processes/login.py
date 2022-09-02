
import logging
import pyautogui
import cv2
import libs.cv2_util as cv2_util

import secrets
from libs.encode import decode, encode

from libs.Session import ProcessInfo, Session
import win32.lib.win32con as win32con
from libs.save_desc import SaveDesc
from processes.core import Core_Info

import PySimpleGUI as sg

# Get refrence images
img_pwdtxt = cv2.imread('../res/imgs/Password_Text.png')
img_palybtn = cv2.imread('../res/imgs/Play_Button.png')

class Login_Info(ProcessInfo):
    save_desc = SaveDesc("Login", ["pwd"])

    def __init__(self, fast_login=False, core="Core"):
        self.state = -1
        self.id = None
        self.pwd = ["", ""]

        self._core_name = core
        self._fast_login = fast_login

        self._window:sg.Window = None
        self._show_pwd = False

def init_login(session:Session, info:Login_Info):
    # Chose method of login atuomation
    if(not info._fast_login):
        # Add Login Hotkey to session (Ctrl+Alt+F)
        info.id = session.add_hotkey(
            ord('F'), win32con.MOD_CONTROL | win32con.MOD_ALT,
            start_login_process, info
        )
        logging.info("Press [Alt+Ctrl+F] to start login process")
    else:
        # Start up laucher detection task
        core_info = session.get_info("Core")
        session.add_task("login_await", await_launcher_task, info, core_info)

    # Return login data object
    return info

def start_login_process(session:Session, info:Login_Info):
    # Check if already running
    if(info.state != -1):
        return

    # Start login task
    logging.info("Starting Login Process")
    info.state = 0
    session.add_task("login_task", login_task, info)
    
    # Disable login keybind
    if(info.id != None):
        session.remove_hotkey(info.id)
        info.id = None

def await_launcher_task(session:Session, info:Login_Info, core_info:Core_Info):
    # Check if launcher is open
    if(core_info.in_launcher):
        # Check if already atempting to login
        if(info.state == -1):
            start_login_process(session, info)
    elif(info.state == 2):
        # Reset state when launcher closes
        info.state = -1
    return True

def login_task(session:Session, info:Login_Info):
    # Get screenshot
    frame = cv2_util.screenshot()

    if(info.state == 0):
        # Check for password field
        found, loc, err = cv2_util.locate(img_pwdtxt, frame, 0.001)
        if(found):
            logging.debug("Login -- Entering Password")
            # Enter password in field
            click_loc = [loc[0]+20, loc[1]+35]
            pyautogui.moveTo(*click_loc)
            pyautogui.click(*click_loc, 1)
            pyautogui.sleep(0.1)
            pyautogui.typewrite(decode(*info.pwd))
            pyautogui.press(["enter"])
            
            info.state = 1
    
    elif(info.state == 1):
        # Check for play button
        found, loc, err = cv2_util.locate(img_palybtn, frame, 0.001)
        if(found):
            logging.debug("Login -- Clicking Play Button")
            # Click on play button
            click_loc = [loc[0]+50, loc[1]+30]
            pyautogui.moveTo(*click_loc)
            pyautogui.click(*click_loc, 1)

            # End login task
            info.state = 2
            logging.info("Login Process Done")
            return False

    return True

def open_password_menue(session:Session, info:Login_Info):
    if(info._window != None): return

    info._show_pwd = False
    info._window = sg.Window("Edit Password", layout=[
        [sg.Text("Password:"), 
            sg.Input(default_text=decode(*(info.pwd)), password_char="*", key="PWD_FIELD"), 
            sg.Button("O",key="SHOW_PWD",font="Consolas")],
        [sg.Button("Close", key="CLOSE"), sg.Button("Save", key="SAVE_PWD")]
    ])

    session.add_task("password_menue_task", password_menue_task, info)

def _cleanup_password_menue(info:Login_Info):
    info._window.close()
    info._window = None
    return False

def password_menue_task(session:Session, info:Login_Info):
    event, values = info._window.read(timeout=0)

    if(event == sg.WIN_CLOSED or event == "CLOSE"):
        return _cleanup_password_menue(info)
    elif(event == "SHOW_PWD"):
        info._show_pwd = not info._show_pwd
        info._window["PWD_FIELD"].update(password_char="" if (info._show_pwd) else "*")
        info._window["SHOW_PWD"].update("0" if (info._show_pwd) else "O")
    elif(event == "SAVE_PWD"):
        key = secrets.token_hex(16)
        pwd_hex = encode(values["PWD_FIELD"], key)
        info.pwd = [pwd_hex, key]
        logging.info("Password Updated!")
        return _cleanup_password_menue(info)

    return True
