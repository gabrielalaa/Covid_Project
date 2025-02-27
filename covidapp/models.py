from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
import os

# Load the key from the file
fernet_key_path = "fernet_key.key"

if os.path.exists(fernet_key_path):
    with open(fernet_key_path, "rb") as key_file:
        keys = key_file.read().splitlines()
        fernet_key = keys[1]  # Second line is Fernet key
else:
    raise ValueError("Fernet key file is missing!")

cipher_suite = Fernet(fernet_key)

class Post(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    content = models.TextField(_("Content"))

class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    hashed_password = models.CharField(max_length=255)
    encrypted_message = models.TextField()

    def set_password(self, raw_password):
        self.hashed_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.hashed_password)

    def set_message(self, message):
        self.encrypted_message = cipher_suite.encrypt(message.encode()).decode()

    def get_message(self):
        return cipher_suite.decrypt(self.encrypted_message.encode()).decode()
