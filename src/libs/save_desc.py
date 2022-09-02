
from genericpath import isfile
import json
import os.path

class SaveDesc:
    def __init__(self, name:str, atribs:list[str]):
        self.name = name
        self.atribs = atribs

class SaveDescManager:
    def __init__(self, path) -> None:
        self._json_data = {}
        self._loaded_json = False
        self._json_path = path
        self._objects = []
        
        # Atempt to load json save file
        if os.path.isfile(path):
            with open(path, "r") as json_file:
                self._loaded_json = True
                try:
                    self._json_data = json.load(json_file)
                except: self._loaded_json = False
    
    def register_obj(self, obj, save_desc:SaveDesc):
        # Check typing
        if(type(save_desc) != SaveDesc):
            raise RuntimeError(f"save_desc -- given is objed of type \"{type(save_desc)}\", should be of type \"{SaveDesc}\".")

        # Read data values into object and save for later
        read_obj_save_desc(obj, save_desc, self._json_data)
        self._objects.append((obj, save_desc))

    def write_save_data(self):
        # Save object data to json
        for obj, save_desc in self._objects:
            write_obj_save_desc(obj, save_desc, self._json_data)

        # Wrinte new json data to file
        with open(self._json_path, "w") as json_file:
            json.dump(self._json_data, json_file)

def read_obj_save_desc(obj, save_desc:SaveDesc, json_data):
    if(not save_desc.name in json_data): return
    obj_dat = json_data[save_desc.name]
    for prop in save_desc.atribs:
        if(not prop in obj_dat): continue
        setattr(obj, prop, obj_dat[prop])

def write_obj_save_desc(obj, save_desc:SaveDesc, json_data):
    obj_dat = {}
    if(save_desc.name in json_data):
        obj_dat = json_data[save_desc.name]
    for prop in save_desc.atribs:
        obj_dat[prop] = getattr(obj, prop)
    json_data[save_desc.name] = obj_dat
