
import time
from libs.save_desc import SaveDescManager

import ctypes
from ctypes import wintypes
import win32.lib.win32con as win32con
user32 = ctypes.windll.user32

class ProcessInfo:
    save_desc = None
    def __init__(self): pass

class Process:
    def __init__(self, name:str, init_func, process_info:ProcessInfo = None) -> None:
        self._name = name
        self._info = process_info
        self._init_func = init_func

    def configure(self, session:'Session'):
        pass

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
        self._rmv_tasks = []

        self._processes = {}
        self._save_desc_mgr = SaveDescManager("../res/config.json")

        self._delta_time = 0

        Session._instance = self
        return self

    def start(self, cleanup_callback = None):
        # Final Setup
        self.cleanup_callback = cleanup_callback
        self._Configure()

        # Main loop
        self.running = True
        while(self.running):
            _cur_time = time.time()
            self._update()
            self._delta_time = time.time() - _cur_time
        self._cleanup()

    def _Configure(self):
        # Initalize processes
        sdm:SaveDescManager = self._save_desc_mgr
        for name, proc in self._processes.items():
            # Load Save Description for Process
            if(proc._info.save_desc != None):
                sdm.register_obj(proc._info, proc._info.save_desc)
            # Init Process
            proc._init_func(self, proc._info)

    def _update(self):
        # Update Hotkey detection
        if user32.PeekMessageA(ctypes.byref(self._msg), None, 0, 0, win32con.PM_REMOVE) != 0:
            if self._msg.message == win32con.WM_HOTKEY:
                msg_id = self._msg.wParam 
                if(msg_id > 0 and msg_id <= len(self._hotkeys)):
                    hotkey = self._hotkeys[msg_id-1]
                    if(hotkey != None):
                        hotkey[3](self, *hotkey[4])
        
        # Add new hotkeys to pool
        for hotkey in self._new_hotkeys:
            if(len(self._hotkeys) < hotkey[0]):
                self._hotkeys.append(hotkey)
            else:
                self._hotkeys[hotkey[0]-1] = hotkey
        self._new_hotkeys = []
        
        # Update Tasks
        stop_list = []
        for name, entry in self._tasks.items():
            if(not entry[0](self, *entry[1])):
                stop_list.append(name)
        for name in stop_list:
            self.remove_task(name)

        # Apply aditional changes to task pool
        for name, callback, args in self._new_tasks:
            self._tasks[name] = (callback, args)
        for name in self._rmv_tasks:
            self._tasks[name] = None
            self._tasks.pop(name)
        self._new_tasks = []
        self._rmv_tasks = []

    def cleanup(self):
        if(self.running):
            self.running = False
            self._cleanup()

    def _cleanup(self):
        # Save out tracked Process Info
        sdm:SaveDescManager = self._save_desc_mgr
        sdm.write_save_data()

        # Cleanup system hotkey objects
        for hotkey in self._hotkeys:
            self.remove_hotkey(hotkey[0])

        # Cleanup callback
        if(self.cleanup_callback != None):
            self.cleanup_callback()

    def add_hotkey(self, key_code:int, mod_code:int, callback, *args) -> bool:
        # Get open hotkey id
        new_hotkey_ids = [nk[0] for nk in self._new_hotkeys]
        open_slots = [i for i in range(0,len(self._hotkeys)) if (self._hotkeys[i] == None) and not(i in new_hotkey_ids)]
        id = len(self._hotkeys)+len(self._new_hotkeys) if len(open_slots) == 0 else open_slots[0]
        id += 1

        # Register hotkey with windows
        if not user32.RegisterHotKey(None, id, mod_code, key_code):
            print(f"Unable to register keycode ({key_code}|{mod_code})({id})")
            return -1
        
        # Store hotkey info
        self._new_hotkeys.append((id, key_code, mod_code, callback, args))
        return id

    def remove_hotkey(self, id) -> bool:
        # Check if valid id
        rmvd = False
        if(id > 0 and id <= len(self._hotkeys)):
            user32.UnregisterHotKey (None, id)
            rmvd = (self._hotkeys[id-1] != None)
            self._hotkeys[id-1] = None
        return rmvd

    def add_task(self, name, callback, *args):
        self._new_tasks.append((name, callback, args))

    def remove_task(self, name):
        self._rmv_tasks.append(name)

    def add_process(self, process:Process):
        self._processes[process._name] = process

    def get_info(self, proc_name:str):
        proc:Process = self._processes[proc_name]
        return proc._info

    @property
    def delta_time(self) -> float:
        return self._delta_time
        
