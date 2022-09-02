
from libs.Session import ProcessInfo, Session

import threading
import subprocess

class Core_Info(ProcessInfo):
    def __init__(self) -> None:
        self.in_launcher = False
        self.in_client = False

        self._tracking_thread = None

class ProcessTrackingTread(threading.Thread):
    def __init__(self, core_info:Core_Info, name="process-tracking-thread") -> None:
        self.running = False
        self.core_info = core_info
        super(ProcessTrackingTread, self).__init__(name=name)

    def run(self) -> None:
        self.running = True
        while self.running:
            # Check if launcher is currently open
            self.core_info.in_launcher = process_exists("ffxivlauncher.exe")
            self.core_info.in_client = process_exists("ffxiv.exe")

def process_exists(process_name):
    try:
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())
    except: pass

def init_core(session:Session, info:Core_Info) -> Core_Info:
    # Start seperate thread for process tracking
    info._tracking_thread = ProcessTrackingTread(info)
    info._tracking_thread.start()

    # Return core data object
    return info
