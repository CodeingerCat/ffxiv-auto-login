import json

import os
from argparse import ArgumentParser
import secrets

from libs.encode import encode

def init_config_dict():
    config = {
        'version' : '1.0.0',
        'user': { 'pwd': ['',''] }
    }
    return config

if __name__ == "__main__":
    CONFIG_PATH = '../res/config.json'

    arg_psr = ArgumentParser()
    arg_psr.add_argument('--password', '-pwd', type=str)
    args = arg_psr.parse_args()

    # Load or create config
    if(not os.path.isfile(CONFIG_PATH)):
        config = init_config_dict()
    else:
        with open(CONFIG_PATH, 'r') as config_file:
            config = json.load(config_file)
        if(config.get('version', None) == None):
            config = init_config_dict()

    # Place in new password
    if(args.password):
        key = secrets.token_hex(16)
        pwd_hex = encode(args.password, key)
        config['user']['pwd'] = [key, pwd_hex]
        print("Password Updated!")

    # Write out new config
    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(config, config_file)
