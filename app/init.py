import subprocess

import connection.internet_connection
import connection.default_ftp_server_connection


if __name__ == "__main__":
    subprocess.run(["python", "app/main.py"])
