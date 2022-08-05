# list[uint8] <--> Ascii String
def str_to_ints(msg:str) -> list[int]:
    return [ord(c) for c in msg]

def ints_to_str(arr: list[int]) -> str:
    return ''.join([chr(v) for v in arr])


# list[uint8] <--> Ascii Hex String
def ints_to_hex(arr: list[int], upper=True, unit_length=2):
    frmt = f'%0{unit_length}{"X" if upper else "x"}'
    return ''.join([frmt%v for v in arr])

def hex_to_ints(hex_str: str, unit_length=2):
    segs = [hex_str[i:i+unit_length] for i in range(0, len(hex_str), unit_length)]
    return [int(v, base=16) for v in segs]


# Ascii String <--> Ascii Hex String
def str_to_hex(msg:str, upper=True, unit_length=2):
    return ints_to_hex(str_to_ints(msg), upper, unit_length)

def hex_to_str(hex_str: str, unit_length=2):
    return ints_to_str(hex_to_ints(hex_str))


# Ascii Hex String -> int
def hex_to_int(hex_str:str):
    return int.from_bytes(hex_to_ints(hex_str), 'little')
