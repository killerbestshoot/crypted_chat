import csv
import getpass
import hashlib
import io
import os
import time

from colorama import Fore, Style

from app.app_home import init_home
import app.json_reader as jr
import app.style.magnify as st

arrow_up, arrow_down, emoji_ok, emoji_login, emoji_loading = st.emoticon()


def init():
    st.header_page()
    print(" " * 35, "login(1) or sign up(2) exit(0)", " " * 35)

    import ftplib
    def check_existing_user(ftp, remote_csv_path, username):
        with io.BytesIO() as file:
            ftp.retrbinary(f"RETR {remote_csv_path}", file.write)
            file.seek(0)
            existing_data = file.read().decode('utf-8')
            existing_users = [line.split(',')[0] for line in existing_data.split('\n')[1:] if line]

            return username in existing_users

    def login():
        settings = jr.load_settings_from_json()
        # charge les paramettres du fichier json (settings.json) qui se trouvent dans le repertoire locale C:
        if settings:
            # verifie si les paremettres existent
            local_directory = settings.get("local_directory")
            ftp_server = settings.get("ftp_server")
            ftp_port = settings.get("ftp_port")
            ftp_username = settings.get("ftp_username")
            ftp_password = settings.get("ftp_password")

            if local_directory:
                # verifie d abord si les paramettres seront sauves en local
                csv_file_path = os.path.join(local_directory, "users.csv")
                username = input(f"Insert your Username {emoji_login} ")
                password = getpass.getpass("Insert your password: ")

                # Si le repertoire local est specifie, essayez de lire le fichier CSV localement
                # Sinon, tentez de vous connecter au serveur FTP
                if os.path.exists(csv_file_path):
                    try:
                        with open(csv_file_path, "r") as file:
                            reade = csv.reader(file)
                            for rows in reade:
                                if rows[0] == username:
                                    hashed_password = rows[1]
                                    submitted_password_hash = hashlib.sha256(password.encode()).hexdigest()
                                    if hashed_password == submitted_password_hash:
                                        print(f"{Fore.GREEN}login successful{Style.RESET_ALL}\n")
                                        print("*" * 99)
                                        init_home(username)
                                        return
                                    else:
                                        print("Username or Password incorrect")
                                        return login()
                            # print("Username or Password incorrect")
                            # return login()

                    except Exception as e:
                        print(f"An error occurred: {e}")
            elif ftp_server and ftp_port:
                username = input(f"Insert your Username {emoji_login} ")
                password = getpass.getpass("Insert your password: ")
                try:
                    ftp = ftplib.FTP()
                    ftp.connect(ftp_server, int(ftp_port))
                    ftp.login(ftp_username, ftp_password)

                    remote_csv_path = "datas/users/users.csv"

                        # Telechargement du fichier CSV du serveur FTP
                    with io.BytesIO() as file:
                        ftp.retrbinary(f"RETR {remote_csv_path}", file.write)
                        file.seek(0)
                        file_content = file.read().decode('utf-8')
                        csv_datas = csv.reader(io.StringIO(file_content))

                        for rowss in csv_datas:
                            if rowss[0] == username:
                                hashed_password = rowss[1]
                                submitted_password_hash = hashlib.sha256(password.encode()).hexdigest()
                                if hashed_password == submitted_password_hash:
                                    print(f"{Fore.GREEN}login successful{Style.RESET_ALL}\n")
                                    print("*" * 99)
                                    init_home(username)
                                    return
                                else:
                                    print("Username or Password incorrect")
                                    return login()
                except ftplib.all_errors as e:
                    print(f"Failed to connect to FTP: {e}")
                    menu()
            else:
                print("No local or FTP directory specified in settings.")
                menu()
        else:
            print("Settings not found.")
            return menu()

    def sign_up():
        settings = jr.load_settings_from_json()
        if settings:
            local_directory = settings.get("local_directory")
            ftp_server = settings.get("ftp_server")
            ftp_port = settings.get("ftp_port")
            ftp_username = settings.get("ftp_username")
            ftp_password = settings.get("ftp_password")

            if local_directory:
                csv_file_path = os.path.join(local_directory, "users.csv")
                username = input("Choose your username: ")
                password = getpass.getpass("Choose a strong password: ")
                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                try:
                    if os.path.exists(csv_file_path):
                        with open(csv_file_path, "r") as file:
                            reader = csv.reader(file)
                            username_exists = False

                            for row in reader:
                                if row[0] == username:
                                    print(
                                        f"{Fore.RED}Please choose a different username; this one is already taken.{Style.RESET_ALL}")
                                    time.sleep(1)
                                    username_exists = True
                                    sign_up()
                                    break

                            if not username_exists:
                                # If the username is not found, add it to the file
                                with open(csv_file_path, "a", newline="") as file:
                                    writer = csv.writer(file)
                                    writer.writerow([username, hashed_password])
                                    print(f"{Fore.GREEN}Sign up successful{Style.RESET_ALL}")
                                    time.sleep(1.5)
                                    menu()

                    else:
                        # Si le fichier n existe pas, creez-le et ajoutez le nouvel utilisateur
                        with open(csv_file_path, "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(["Username", "Hashed_Password"])  # En-tête du fichier CSV
                            writer.writerow([username, hashed_password])
                            print(f"{Fore.GREEN}Sign up successful{Style.RESET_ALL}")
                            time.sleep(1)
                            menu()
                            # Effectuez ici l action de votre menu

                except IOError as e:
                    print(f"An error occurred: {e}")
            elif ftp_server and ftp_port:
                username = input("Choose your username: ")
                password = getpass.getpass("Choose a strong password: ")
                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                try:
                    ftp = ftplib.FTP()
                    ftp.connect(ftp_server, int(ftp_port))
                    ftp.login(ftp_username, ftp_password)

                    remote_csv_path = "datas/users/users.csv"
                    start_path = "datas/users"

                    file_list = ftp.nlst(start_path)

                    if "users.csv" not in file_list:
                        initial_content = "username,password_hash\n"
                        with io.BytesIO(initial_content.encode('utf-8')) as file:
                            ftp.storbinary(f"STOR {remote_csv_path}", file)
                        print("users.csv created on the FTP server.")
                        print(file_list)
                        time.sleep(2)

                    user_exists = check_existing_user(ftp, remote_csv_path, username)

                    if user_exists:
                        print("Username already exists. Please choose a different username.")
                        return sign_up()
                    else:
                        content = f"{username},{hashed_password}\n"
                        content_as_bytes = content.encode('utf-8')

                        with io.BytesIO(content_as_bytes) as file:
                            ftp.storbinary(f"APPE {remote_csv_path}", file)
                        print(f"User {Fore.MAGENTA}{username}{Style.RESET_ALL} added to users.csv on the FTP server.")
                        time.sleep(2)
                        menu()

                except Exception as e:
                    print(f"Failed to connect to FTP: {e}")
                    menu()

            else:
                print("No local or FTP directory specified in settings.")
                return
        else:
            print("Settings not found.")
            return

    def menu():
        while True:
            choice = input("Make your Choice: ")

            if choice == "1":
                login()
                break
            elif choice == "2":
                sign_up()
                break
            elif choice == "0":
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")

    menu()
