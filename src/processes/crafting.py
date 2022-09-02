
import logging
import pyautogui

from libs.Session import Session, ProcessInfo
import win32.lib.win32con as win32con

import PySimpleGUI as sg
from libs.save_desc import SaveDesc
from libs.simple_gui_util import sgIntField, sgFieldBank
from processes.core import Core_Info

class Crafting_Info(ProcessInfo):
    save_desc = SaveDesc("Crafting", ["craft_count","craft_time","window_location"])
    def __init__(self):
        self.hotkey_id = None
        self.prompt_open = False

        self.craft_count = 1
        self.done_count = 0
        self.craft_time = 6

        self.window = None
        self.window_location = [0,0]
        self.fields:sgFieldBank = None


def init_crafting(session:Session, info:Crafting_Info):
    # Add Login Hotkey to session (Ctrl+Alt+F)
    info.hotkey_id = session.add_hotkey(
        ord('L'), win32con.MOD_CONTROL | win32con.MOD_ALT,
        open_crafting_menue, info
    )

    # Setup staring conditions
    info.done_count = info.craft_count

    # Return login data object
    return info

def open_crafting_menue(session:Session, info:Crafting_Info):
    if((not info.prompt_open) and (info.done_count == info.craft_count)):
        layout = [
            [sg.Text("Craft Prompt")],
            [sg.Text("Craft Count:"), sg.Input(str(info.craft_count),key="CRAFT_COUNT",tooltip="Number of items to craft")],
            [sg.Text("Craft Time:"), sg.Input(str(info.craft_time),key="CRAFT_TIME",tooltip="Time of craft in seconds")],
            [sg.Text("", key="WARN_MSG", visible=False)],
            [sg.Button("Close"), sg.Button("Start")]
        ]

        window = sg.Window(title="Craft Prompt", layout=layout, location=info.window_location)
        info.window = window
        info.prompt_open = True

        info.fields = sgFieldBank([
            sgIntField(key="CRAFT_COUNT", range=(0,None)),
            sgIntField(key="CRAFT_TIME", range=(0,None))
        ])

        session.add_task("prompt_crafting_task", prompt_crafting_task, info)

def prompt_crafting_task(session:Session, info:Crafting_Info):
    # Update window state
    window:sg.Window = info.window
    event, values = window.read(timeout=0)

    # Hanle window close request
    if event == "Close" or event == sg.WIN_CLOSED:
        info.prompt_open = False
        info.window.close()
        return False

    # Update info
    info.fields.update(values)
    info.window_location = window.CurrentLocation()

    # Display user warnings
    if(not info.fields.is_valid()):
        window['WARN_MSG'].update(info.fields.warning_text, visible=True)
    else: window['WARN_MSG'].update(visible=False)

    # Handle start button press
    if (event == "Start") and (info.fields.is_valid()):
        if(info.fields['CRAFT_COUNT'] > 0):
            # Load values
            info.craft_count = info.fields['CRAFT_COUNT']
            info.craft_time = info.fields['CRAFT_TIME']
            info.done_count = 0

            # Start task
            print(f"Crafting {info.craft_count} itmes")
            session.add_task("crafting_task", crafting_task, info)
        else:
            logging.warn("Valid craft counts are 1 and up.")

        # Close prompt
        info.prompt_open = False
        info.window.close()
        return False


    return True

def crafting_task(session:Session, info:Crafting_Info):
    # Click to start craft
    pyautogui.click(clicks=2, interval=0.1) 
    pyautogui.sleep(1.2)

    # Use hotkey to start macro
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyDown('_')
    pyautogui.sleep(0.1)
    pyautogui.keyUp('_')
    pyautogui.keyUp('Ctrlleft')

    # Wait for craft compleation
    pyautogui.sleep(info.craft_time)
    print(f"Crafted [{info.done_count+1}\{info.craft_count}]")
    
    # Wait to return to main craft menue
    pyautogui.sleep(3)

    # Update craft count and loop
    info.done_count += 1
    if(info.done_count >= info.craft_count): print("Crafting Done")
    return (info.done_count < info.craft_count)
