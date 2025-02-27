from cryptography.fernet import Fernet
import secrets
import os

key_path = "fernet_key.key"

# Check if the key file already exists
if os.path.exists(key_path):
    print("Key file already exists. No changes made.")
else:
    # Generate a new encryption key for Fernet
    fernet_key = Fernet.generate_key()

    # Generate a secure Django SECRET_KEY
    secret_key = secrets.token_urlsafe(50)

    # Save both keys in the file
    with open(key_path, "wb") as key_file:
        key_file.write(secret_key.encode() + b"\n" + fernet_key)

    print("New keys generated and saved to 'fernet_key.key'")
    print("Keep this file secure! Do NOT share it publicly.")
