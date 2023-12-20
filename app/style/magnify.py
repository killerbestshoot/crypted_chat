import os
from datetime import datetime, date

current_date = date.today()


def emoticon():
    arrow_up = "\U0001F53C"
    arrow_down = "\U0001F53D"
    emoji_ok = "\U0001F44C"  # ? ou \U0001F44C
    emoji_login = "\U0001F464"  # ? ou \U0001F464
    emoji_loading = "\U0000231B"  # ? ou \U0000231B
    return arrow_up, arrow_down, emoji_ok, emoji_login, emoji_loading


def clear_screen():
    if os.name == 'nt':
        os.system('cls')  # Effacer l'écran sur Windows
    else:
        os.system('clear')  # Clear the screen


def PrintLetter(message):
    print(message, end='', flush=True)


def header_page():
    print("*" * 35, "Welcome to the Shadow Chat ", "*" * 35)
    print("*" * 99)
    print("\n")


def say_hello(username):
    print(f"\nhello connected as {username} at {current_date}\n")
