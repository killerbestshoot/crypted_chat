import contextlib
import sys
import time
# import emoji


import speedtest
from tqdm import tqdm

from app.style.magnify import emoticon, clear_screen
from app.Auth import init

# from app.app_home import init_home()


arrow_up, arrow_down, emoji_ok, emoji_login, emoji_loading, asterisk, hash_symbol, check_mark, heart, speedometer, danger = emoticon()

if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)


def simulate_loading():
    try:

        for _ in tqdm(range(6), desc="Connecting", unit="s"):
            time.sleep(1)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def measure_speed():
    try:
        print("Measuring connection speed...")

        # Utilisation de speedtest-cli pour mesurer la vitesse
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1024 / 1024  # Conversion en Mbps
        upload_speed = st.upload() / 1024 / 1024  # Conversion en Mbps

        return download_speed, upload_speed
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def connect_and_measure_speed():
    with contextlib.suppress(Exception):
        print(f"Connecting...{emoji_loading}")
    if simulate_loading():
        print(f"Connected! {emoji_ok}")
        download_speed, upload_speed = measure_speed()
        if download_speed is not None and upload_speed is not None:
            print(
                f"Your network connection speed: {download_speed:.2f} Mbps {arrow_up} | {upload_speed:.2f} Mbps {arrow_down}")
            time.sleep(3.55)
            clear_screen()
            init()
        else:
            print("Unable to measure speed.")
            time.sleep(2)
            clear_screen()
            init()
    else:
        print("Connection failed. Please check your internet connection.")
        time.sleep(2)
        sys.exit()


connect_and_measure_speed()

# print(os.listdir('../style'))
