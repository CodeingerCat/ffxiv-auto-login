
from libs.Session import process_exists

core_info = {
    'in_launcher':False,
    'in_client':False
}

def init_core(session):
    # Init process tracking task
    session.add_task("process_tracking", process_tracker_task, core_info)

    # Return core data object
    return core_info


def process_tracker_task(session, core_info):
    # Check if launcher is currently open
    core_info['in_launcher'] = process_exists("ffxivlauncher.exe")
    core_info['in_client'] = process_exists("ffxiv.exe")
    return True
