
import win32.lib.win32con as win32con
import ctypes
from ctypes import wintypes
import subprocess

user32 = ctypes.windll.user32

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

class Session:
    _instance = None
    def __new__(cls):
        if(Session._instance != None):
            return Session._instance

        self = object.__new__(cls)
        self.running = False
        
        self._hotkeys = []
        self._new_hotkeys = []
        self._msg = wintypes.MSG()

        self._tasks = {}
        self._new_tasks = []

        Session._instance = self
        return self

    def start(self):
        self.running = True
        while(self.running):
            self._update()
        self._cleanup()

    def _update(self):
        # Update Hotkey detection
        if user32.PeekMessageA(ctypes.byref(self._msg), None, 0, 0, win32con.PM_REMOVE) != 0:
            if self._msg.message == win32con.WM_HOTKEY:
                msg_id = self._msg.wParam 
                if(msg_id > 0 and msg_id <= len(self._hotkeys)):
                    hotkey = self._hotkeys[msg_id-1]
                    if(hotkey != None):
                        hotkey[3](self, *hotkey[4])
        for hotkey in self._new_hotkeys:
            self._hotkeys.append(hotkey)
        
        # Update Tasks
        stop_list = []
        for name, entry in self._tasks.items():
            if(not entry[0](self, *entry[1])):
                stop_list.append(name)
        for name in stop_list:
            self.remove_task(name)
        for name, callback, args in self._new_tasks:
            self._tasks[name] = (callback, args)
                

    def _cleanup(self):
        for hotkey in self._hotkeys:
            self.remove_hotkey(hotkey[0])

    def add_hotkey(self, key_code:int, mod_code:int, callback, *args) -> bool:
        # Get open hotkey id
        open_slots = [i for i in range(0,len(self._hotkeys)) if self._hotkeys == None]
        id = len(self._hotkeys) if len(open_slots) == 0 else open_slots[0]
        id += 1

        # Register hotkey with windows
        if not user32.RegisterHotKey(None, id, mod_code, key_code):
            print(f"Unable to register keycode ({key_code}|{mod_code})({id})")
            return -1
        
        # Store hotkey info
        self._new_hotkeys.append((id, key_code, mod_code, callback, args))
        return id

    def remove_hotkey(self, id):
        # Check if valid id
        if(id > 0 and id <= len(self._hotkeys)):
            user32.UnregisterHotKey (None, id)
            self._hotkeys[id-1] = None

    def add_task(self, name, callback, *args):
        self._new_tasks.append((name, callback, args))

    def remove_task(self, name):
        self._tasks[name] = None
        self._tasks.pop(name)


        
