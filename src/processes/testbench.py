
from ctypes import alignment
import logging
import pyautogui

from libs.Session import Session, ProcessInfo
import win32.lib.win32con as win32con

import easygui
import PySimpleGUI as sg
from libs.save_desc import SaveDesc
from libs.simple_gui_util import sgIntField, sgFieldBank
from processes.core import Core_Info

import copy

class Testbench_Info(ProcessInfo):
    save_desc = SaveDesc("Testbench", ["cur_page", "counter", "position"])

    def __init__(self):        
        self.window:sg.Window = None
        self.window_task = None

        self.layouts = {}
        self.cur_page = "Page_1"

        self.counter = 0.0
        self.position = [0,0]

def init_testbench(session:Session, info:Testbench_Info):
    info.layouts = {
        "Page_1":[
            [sg.Button("Counter Start", expand_x=True)]
        ],
        "Page_2":[
            [sg.Text("0.00", key="TIMER_TEXT", expand_x=True, justification="center", font="Hyvelica 17")]
        ]
    }

    session.add_task("testbench_task", testbench_task, info)
    return info

def open_testbench_window(session:Session, info:Testbench_Info):
    _create_window(info)
    session.add_task("testbench_window_task", testbench_window_task, info)
    return True

def testbench_task(session:Session, info:Testbench_Info):
    if(info.cur_page == "Page_2"):
        info.counter = max(0, info.counter - session.delta_time)
        if(info.counter == 0):
            _reload_window("Page_1", info)
        elif((info.window != None) and (not info.window.is_closed())):
            info.window["TIMER_TEXT"].update(_gen_time_str(info.counter))

    return True

def testbench_window_task(session:Session, info:Testbench_Info):
    event, values = info.window.read(timeout=0)

    if(event == "Counter Start"):
        info.counter = 10.0
        _reload_window("Page_2", info)

    if(event == sg.WINDOW_CLOSED):
        info.window.close()
        return False

    info.position = info.window.CurrentLocation()
    return True


def _create_window(info:Testbench_Info):
    info.window = sg.Window("Test Window", 
        layout=copy.deepcopy(info.layouts[info.cur_page]),
        size=(240,40),
        location = info.position
    )
    info.window.finalize()

def _reload_window(page, info:Testbench_Info):
    info.cur_page = page
    info.position = info.window.CurrentLocation()
    info.window.close()
    _create_window(info)

def _gen_time_str(time):
    t = int(time * 100)
    hour = t//(60*60*100)
    minute = (t//(60*100))%(60)
    second = (t//(100))%(60)
    mil = (t)%(100)
    return f"{hour:02d}:{minute:02d}:{second:02d}.{mil:02d}"