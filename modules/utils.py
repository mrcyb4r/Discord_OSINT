import re
import datetime

colors = {
    "red": "\033[91m",
    "light_red": "\033[91m",
    "orange": "\033[93m",
    "yellow": "\033[93m",
    "green": "\033[92m",
    "light_green": "\033[92m",
    "blue": "\033[94m",
    "light_blue": "\033[94m",
    "purple": "\033[95m",
    "light_purple": "\033[95m",
    "cyan": "\033[96m",
    "light_cyan": "\033[96m",
    "white": "\033[97m",
    "light_white": "\033[97m",
    "black": "\033[90m",
    "grey": "\033[90m",
    "reset": "\033[0m"
}

def print_positive(message, indent=0):
    print("   "*indent + f"{colors['grey']}[{colors['green']}+{colors['grey']}] {colors['green']}{message}{colors['reset']}")

def print_neutral(message, indent=0):
    print("   "*indent + f"{colors['grey']}[{colors['yellow']}*{colors['grey']}] {colors['yellow']}{message}{colors['reset']}")

def print_negative(message, indent=0):
    print("   "*indent + f"{colors['grey']}[{colors['red']}-{colors['grey']}] {colors['red']}{message}{colors['reset']}")
    
def print_result(message, indent=0):
    print("   "*indent + f"{colors['grey']}[{colors['cyan']}~{colors['grey']}] {colors['cyan']}{message}{colors['reset']}")

def print_found(message, indent=0):
    print("   "*indent + f"{colors['grey']}[{colors['blue']}!{colors['grey']}] {colors['blue']}{message}{colors['reset']}")

def print_info(message, indent=0):
    print("   "*indent + f"{colors['grey']}[{colors['light_purple']}i{colors['grey']}] {colors['light_purple']}{message}{colors['reset']}")

def get_links(text):
    return re.findall(r'(https?://[^\s]+)', text)

def get_emails(text):
    return re.findall(r'[\w\.-]+@[\w\.-]+', text)

def convert_unix(milliseconds):
    return datetime.datetime.utcfromtimestamp(milliseconds // 1000).strftime('%m/%d/%Y, %H:%M:%S')