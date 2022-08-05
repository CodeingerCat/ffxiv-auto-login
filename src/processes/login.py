
import logging
import pyautogui
import cv2
import libs.cv2_util as cv2_util

from libs.encode import decode

from libs.Session import Session
import win32.lib.win32con as win32con

# Get refrence images
img_pwdtxt = cv2.imread('../res/imgs/Password_Text.png')
img_palybtn = cv2.imread('../res/imgs/Play_Button.png')

class Login_Info:
    def __init__(self):
        self.state = -1
        self.id = None
        self.pwd = ''
login_info = Login_Info()

def init_login(session:Session, config, core_info, fast_login):
    # Decode password
    pwd_key, pwd_hex = config['user']['pwd']
    login_info.pwd = decode(pwd_hex, pwd_key)

    # Chose method of login atuomation
    if(not fast_login):
        # Add Login Hotkey to session (Ctrl+Alt+F)
        login_info.id = session.add_hotkey(
            ord('F'), win32con.MOD_CONTROL | win32con.MOD_ALT,
            start_login_process, login_info
        )
    else:
        # Start up laucher detection task
        session.add_task("login_await", await_launcher_task, core_info, login_info)

    # Return login data object
    return login_info

def start_login_process(session:Session, login_info:Login_Info):
    # Check if already running
    if(login_info.state != -1):
        return

    # Start login task
    logging.info("Starting Login Process")
    login_info.state = 0
    session.add_task("login_task", login_task, login_info)
    
    # Disable login keybind
    if(login_info.id != None):
        session.remove_hotkey(login_info.id)
        login_info.id = None

def await_launcher_task(session:Session, core_info, login_info:Login_Info):
    # Check if launcher is open
    if(core_info['in_launcher']):
        # Check if already atempting to login
        if(login_info.state == -1):
            start_login_process(session, login_info)
    elif(login_info.state == 2):
        # Reset state when launcher closes
        login_info.state = -1
    return True

def login_task(session:Session, login_info):
    # Get screenshot
    frame = cv2_util.screenshot()

    if(login_info.state == 0):
        # Check for password field
        found, loc, err = cv2_util.locate(img_pwdtxt, frame, 0.001)
        if(found):
            # Enter password in field
            click_loc = [loc[0]+20, loc[1]+35]
            pyautogui.moveTo(*click_loc)
            pyautogui.click(*click_loc, 1) 
            pyautogui.typewrite(login_info.pwd)
            pyautogui.press(["enter"])
            
            login_info.state = 1
    
    elif(login_info.state == 1):
        # Check for play button
        found, loc, err = cv2_util.locate(img_palybtn, frame, 0.001)
        if(found):
            # Click on play button
            click_loc = [loc[0]+50, loc[1]+30]
            pyautogui.moveTo(*click_loc)
            pyautogui.click(*click_loc, 1)

            # End login task
            login_info.state = 2
            logging.info("Login Process Done")
            return False

    return True
