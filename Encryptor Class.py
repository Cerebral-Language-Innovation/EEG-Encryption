from cryptography.fernet import Fernet


# class for cryptography functions that we can use with csv files

class Encryptor():
    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):  # key_name is a keyfile: keyone.key
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key

    def file_encrypt(
            self, key, original_file, encrypted_file
    ):  # original_file is the eeg data in csv format, then encrypted_file is the data encrypted (also csv format)

        f = Fernet(key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open(encrypted_file, 'wb') as file:
            file.write(encrypted)

    def file_decrypt(self, key, encrypted_file, decrypted_file):
        f = Fernet(key)

        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()

        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, 'wb') as file:
            file.write(decrypted)