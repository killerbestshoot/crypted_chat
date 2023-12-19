import ftplib

def connect_ftp():
    ftp_server = '127.0.0.1'
    ftp_port = 21  # Le port par défaut pour FTP est 21
    ftp_username = 'secret'
    ftp_password = '<PASSWORD>'

    try:
        return ftplib.FTP(ftp_server, ftp_username, ftp_password)
    except ftplib.all_errors as e:
        # Vous pouvez affiner cette exception pour une gestion spécifique des erreurs FTP
        raise ConnectionError(f"Failed to connect to the FTP server: {e}") from e
