import PySimpleGUI as sg

def _check_int(s):
    if len(s) == 0: return False
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

class sgField:
    _auto_key_id = 1

    def __init__(self, name:str|None=None, key:str|None=None) -> None:
        # Setup field tracking key
        if(key == None):
            key = f"KEY_{sgField._auto_key_id}"
        self._key = key

        self.name = name if (name != None) else (" ".join(key.split('_'))).title()

        # Setup common value variables
        self._raw_val = ""
        self._valid = ""
        self._wrn_msg = ""
        self.value = None

    def update(self, value_dict) -> None:
        self._raw_val = value_dict[self._key]

    def is_valid(self) -> bool:
        return self._valid

    def get_warn_msg(self) -> str:
        return self._wrn_msg
        
class sgIntField(sgField):
    def __init__(self, name:str|None=None, key:str|None=None, range=(None,None)) -> None:
        self.range = range
        super().__init__(name, key)
        self.value = 0
    
    def update(self, value_dict) -> None:
        super().update(value_dict)

        # Validate value is Int
        self._valid = False
        if(not _check_int(self._raw_val)):
            self._wrn_msg = f"{self.name} must be a whole number."
        else:
            # Validate if value is in range
            val = int(self._raw_val)
            if((self.range[0] != None) and (val <= self.range[0])):
                self._wrn_msg = f"{self.name} must be greater than {self.range[0]}."
            elif((self.range[1] != None) and (val >= self.range[1])):
                self._wrn_msg = f"{self.name} must be less than {self.range[1]}."
            else:
                self._valid = True
                self.value = val

class sgFieldBank:
    def __init__(self, fields=[]) -> None:
        self._fields = {}
        self._err_count = 0
        self.warning_text = ""

        for field in fields:
            self.add_field(field)
    
    def update(self, value_dict):
        self._err_count = 0
        wrn_txt = []
        for name, field in self._fields.items():
            field.update(value_dict)
            if(not field.is_valid()):
                self._err_count += 1
                wrn_txt.append(field.get_warn_msg())
        self.warning_text = "\n".join(wrn_txt)

    def is_valid(self):
        return (self._err_count == 0)

    def add_field(self, field:sgField):
        self._fields[field._key] = field

    def __getitem__(self, key:str):
        return self._fields[key].value

