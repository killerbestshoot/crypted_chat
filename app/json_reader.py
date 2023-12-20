import csv
import json
import os

home_directory = os.getenv("HOME")  # Recupere le repertoire personnel de l utilisateur
desktop_path = os.path.join(home_directory, "Desktop/settings.json")  # Concatene avec le repertoire du bureau

def save_settings_to_json(settings):
    try:
        if os.path.exists(desktop_path):
            with open(desktop_path, "r") as json_file:
                existing_settings = json.load(json_file)
                existing_settings.update(settings)
                settings = existing_settings

        with open(desktop_path, "w") as json_file:
            json.dump(settings, json_file)
            print(f"Settings saved to {desktop_path}")
    except Exception as e:
        print(f"Error while saving settings: {e}")



def load_settings_from_json():

    try:
        settings = {}
        if os.path.exists(desktop_path):
            with open(desktop_path, 'r') as file:
                # Vérifie si le fichier est vide ou non avant de le charger
                if os.stat(desktop_path).st_size != 0:
                    settings = json.load(file)
        else:
            with open(desktop_path, 'w') as file:
                json.dump(settings, file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading settings: {e}")
        # Vous pouvez choisir de retourner un dictionnaire vide ou une valeur par defaut en cas d erreur
        return settings  # Retourne un dictionnaire vide si une erreur survient

    return settings



def initiate_msg_log():
    messages_path = "./datas/messages.csv"

    # Extraction du repertoire depuis le chemin du fichier
    directory = os.path.dirname(messages_path)

    # Cree le répertoire s il n existe pas
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Cree le fichier CSV s il n existe pas et ecrit l en-tete
    if not os.path.exists(messages_path):
        with open(messages_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["message_id", "username", "message_content", "timestamp"])
            # Ajoutez d autres lignes au besoin

        return True

def log():
    log_path = "./datas/log.csv"

    # Extraction du repertoire depuis le chemin du fichier
    directory = os.path.dirname(log_path)

    # Cree le repertoire s il n existe pas
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Cree le fichier CSV s il n existe pas et ecrit l en-tete
    if not os.path.exists(log_path):
        with open(log_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "duration", "message_sent", "log_timestamp", "log_ou_timestamp"])
            # Ajoutez d autres lignes au besoin

        return True