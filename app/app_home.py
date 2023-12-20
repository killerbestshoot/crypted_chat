import io
import sys
import time

from colorama import Fore, Style
from app.connection.default_ftp_server_connection import connect_ftp
from app.key_gen import generate_unique_key


def init_home(myusername):
    def check_existing_user(ftp, remote_csv_path, username):
        with io.BytesIO() as file:
            ftp.retrbinary(f"RETR {remote_csv_path}", file.write)
            file.seek(0)
            existing_data = file.read().decode('utf-8')
            existing_users = [line.split(',')[0] for line in existing_data.split('\n')[1:] if line]

            return username in existing_users

    def initiate_dm():
        remote_csv_path = "datas/users/users.csv"
        ftp = connect_ftp()
        print("Initiating dm mode")
        user_to_dm = input("Please insert the username you would like to chat with")
        if check_existing_user(ftp, remote_csv_path, user_to_dm):
            print("the dm has been initialized")
            time.sleep(1)
        else:
            print(f"{Fore.RED}the username provided doesn't match our records please try an other !!!{Style.RESET_ALL}")
            menu()

    def connect_dm():
        remote_csv_path = "datas/users/users.csv"
        ftp = connect_ftp()
        user_to_dm = input("Please insert the username you would like to chat with")
        print("Connecting")
        time.sleep(1)
        if check_existing_user(ftp, remote_csv_path, user_to_dm):
            print(f"Connected to the chat with {user_to_dm}")
            time.sleep(2)
        else:
            print("the username provided doesn't match our chat records")
            time.sleep(1)
            menu()

    def initiate_group_chat():
        remote_csv_path = ""
        group_chat_name = input("Please insert the group name you would like to chat with >")
        print("initializing group chat")
        time.sleep(1)
        # Utilisation pour generer une cle unique de 25 caracteres (20 + len('room_'))
        unique_access_key = generate_unique_key(30)
        print(f"Unique Access Key: {Fore.BLUE}{unique_access_key}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}keep it safe !!!{Style.RESET_ALL}")

    def menu():
        print("1. Initiate direct chat")
        print("2. Connect to a direct chat")
        print("3. Initiate group chat")
        print("4. Connect to group chat")
        print("5. Verify if you have any messages ")
        print("0. Exit")
        while True:
            choice = input("\nWould you like to ? >")
            if choice == "1":
                initiate_dm()
                break
            elif choice == "2":
                connect_dm()
                break
            elif choice == "3":
                initiate_group_chat()
                break
            elif choice == "4":
                pass
            elif choice == "5":
                pass
            else:
                print("Invalid")
                break

    menu()
