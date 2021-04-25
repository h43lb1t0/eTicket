from datetime import datetime
from pprint import pprint
import json


def log(message):
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(f"==> {dt_string} Log: {message}")


def debug(module, message):
    print("")
    pprint(f"    !==> DEBUG LOG for Module: {module}, Message: {message}")
    print("")
