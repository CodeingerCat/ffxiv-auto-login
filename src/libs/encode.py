from random import Random
from libs.str_util import hex_to_int, hex_to_ints, str_to_ints, ints_to_hex, ints_to_str

def encode(msg:str, key:str) -> str:
    rng = Random(hex_to_int(key))
    vals = str_to_ints(msg)
    vals_enc = [(x + rng.randint(0,255))%256 for x in vals]
    return ints_to_hex(vals_enc)

def decode(hex_msg:str, key:str) -> str:
    rng = Random(hex_to_int(key))
    vals_enc = hex_to_ints(hex_msg)
    vals = [(x - rng.randint(0,255))%256 for x in vals_enc]
    return ints_to_str(vals)
