import json
import os
import subprocess
import sys
import time
from ftplib import FTP

from colorama import Fore, Style

import app.json_reader as jr


# def create_users_file(directory):
#     users_path = os.path.join(directory, "users.csv")
#     with open(users_path, "w"):
#         pass
#
#
# def create_messages_file(directory):
#     messages_path = os.path.join(directory, "messages.csv")
#     with open(messages_path, "w"):
#         pass
#
#
# def update_or_create_settings(directory):
#     settings_file = "settings.json"
#
#     if os.path.exists(settings_file):
#         with open(settings_file, "r") as file:
#             settings = json.load(file)
#     else:
#         settings = {}
#
#     settings["local_directory"] = directory
#
#     with open(settings_file, "w") as file:
#         json.dump(settings, file)
#         print("Settings updated in settings.json")
#
#
# def default_directory_choice():
#     try:
#         root_directory = "C:"  # Chemin racine
#         if not os.path.exists(root_directory):
#             os.makedirs(root_directory)
#
#         os.chdir(root_directory)
#         create_users_file(root_directory)
#         create_messages_file(root_directory)
#         print(f"Files will be saved locally in: {root_directory}")
#
#         # Enregistrement du parametre dans un fichier JSON
#         update_or_create_settings(root_directory)
#
#     except FileNotFoundError:
#         print("The specified directory path is invalid.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


def local_directory_choice():  # sourcery skip: extract-method
    while True:
        local_directory = input("Enter the local directory path to save the files: ")
        try:
            if os.path.exists(local_directory) and os.path.isdir(local_directory):
                os.chdir(local_directory)

                settings = {"local_directory": local_directory}
                if jr.save_settings_to_json(settings):
                    print(f"Files will be saved locally in: {local_directory}")

            while True:
                continue_option = input("Do you want to try another path? (Y/N): ")
                if continue_option.upper() == "N":
                    return
                elif continue_option.upper() == "Y":
                    break
                else:
                    print("Invalid choice. Please enter Y or N.")
        except FileNotFoundError:
            print("The specified directory path is invalid.")
        except Exception as e:
            print(f"An error occurred: {e}")


def test_ftp_connection(ftp_server, ftp_port, ftp_username, ftp_password):
    try:
        with FTP() as ftp:
            ftp.connect(ftp_server, int(ftp_port))
            ftp.login(ftp_username, ftp_password)
            return True
    except Exception as e:
        print(f"{Fore.RED}FTP connection failed: {e}{Style.RESET_ALL}")
        return False


def remote_directory_choice():
    while True:
        try:
            ftp_server = input("Enter FTP server address: ")
            ftp_port = input("Enter the ftp port: ")
            ftp_username = input("Enter FTP username: ")
            ftp_password = input("Enter FTP password: ")

            # Verification de la connexion au serveur FTP
            if test_ftp_connection(ftp_server, ftp_port, ftp_username, ftp_password):
                print(f"{Fore.BLUE}Connected to FTP server: {ftp_server}{Style.RESET_ALL}")

                # Si la connexion reussit, enregistrez les parametres dans un fichier JSON
                settings = {"ftp_server": ftp_server, "ftp_port": ftp_port, "ftp_username": ftp_username, "ftp_password": ftp_password}
                if jr.initiate_msg_log() and jr.log():
                    jr.save_settings_to_json(settings)
            else:
                print(
                    f"{Fore.RED}Connection to FTP server failed. Please check your credentials.{Style.RESET_ALL}"
                )
            while True:
                continue_option = input("Do you want to try another path? (Y/N): ")
                if continue_option.upper() == "N":
                    return  # Retour au menu principal
                elif continue_option.upper() == "Y":
                    break  # Reexecute remote_directory_choice
                else:
                    print("Invalid choice. Please enter Y or N.")
        except Exception as e:
            print(f"An error occurred: {e}")


def main_menu():
    while True:
        print("Welcome to the CryptedChat")
        print("Some configuration settings you would like to use:\n")
        print("this setting mode appear once\n")
        print("Choose where to save the files:")
        print("1. Local")
        print("2. Remote (FTP Server)")
        print("3. Default settings")
        print("4. Save setting and Continue")
        print(f"{Fore.YELLOW}0. Exit{Style.RESET_ALL}")
        choice = input("Enter your choice (1,2,3 or 0): ")

        if choice == "1":
            local_directory_choice()
        elif choice == "2":
            remote_directory_choice()
        elif choice == "3":
            print("You choose use the default settings ")
            # default_directory_choice()
        elif choice == "4":
            subprocess.run(["python", "app/connection/Internet_connection.py"])
        elif choice == "405":
            print("You do not have permission to enter this section if you have it")
            attempts = 0
            while attempts < 3:
                pass_key = input("Insert the required password: ")
                if pass_key == "Password":
                    print("You have entered the Administrator mode with all privileges")
                    sys.exit()
                attempts += 1

            if attempts == 3:
                print(f"{Fore.RED}Too many attempts. Exiting this section in 3 seconds...{Style.RESET_ALL}")
                time.sleep(3)
        elif choice == "0":
            print("Exiting")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1,2 or 3 (0) to stop the program.")

if saved_settings := jr.load_settings_from_json():
        # print("Loaded settings:", saved_settings)
        # time.sleep(3)
    subprocess.run(["python", "app/connection/Internet_connection.py"])
else:
    print("No settings found. Proceed to main menu.")
    time.sleep(3)
    main_menu()