import os
from cryptography.fernet import Fernet

def decryptFile(data_file, key_file):
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials')
    data_path = os.path.join(dir_path, data_file)
    key_path = os.path.join(dir_path, key_file)

    if not os.path.exists(key_path):
        print("Error decrypting file: key file does not exist")
        return None
    if not os.path.exists(data_path):
        print("Error decrypting file: data file does not exist")
        return None

    f = open(key_path, "rb")
    key = f.read()
    f.close()

    cipher = Fernet(key)

    f = open(data_path, "rb")
    encrypted_data = f.read()
    f.close()
    data = cipher.decrypt(encrypted_data)
    return data.decode()

