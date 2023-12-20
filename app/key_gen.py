import secrets
import string

def generate_unique_key(length=20):
    prefix = "room_"
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    unique_key = ''.join(secrets.choice(alphabet) for _ in range(length - len(prefix)))
    return prefix + unique_key


