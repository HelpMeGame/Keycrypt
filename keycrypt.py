import binascii

import cryptography.fernet
from cryptography.fernet import Fernet
import os

key = None


def check_key():
    global key
    for r, d, f in os.walk(os.curdir):
        if r != ".":
            return False
        for file in f:
            if "." not in file:
                with open(file, "rb") as stream:
                    key = Fernet(stream.read().decode('utf-8'))
                    return True
    else:
        return False


def main():
    if not check_key():
        print("Key file not found, generating new key...")
        new_key()
        input("Press [ENTER] to close.\n")
        return
    else:
        i = input("Encrypt, Decrypt, or new key? [e/d/k]: ").lower()
        x = True
        if i == "e":
            encrypt()
        elif i == "d":
            x = decrypt()
        elif i == "k":
            new_key()

        if not x:
            print("\nOne or more operations failed.")
        else:
            print("\nCompleted.")
        input("Press [ENTER] to close.\n")


def encrypt():
    for r, d, f in os.walk(os.curdir):
        if r == "." or "venv" in r or ".idea" in r:
            continue
        for file in f:
            location = f"{r}\\{file}"
            with open(location, "rb") as r_stream:
                plaintext = r_stream.read()
            with open(location, "wb") as w_stream:
                w_stream.write(key.encrypt(plaintext))

            os.rename(location, f"{r}\\{key.encrypt(bytes(file.encode('utf-8'))).decode('utf-8')}")


def decrypt():
    all_succeed = True
    for r, d, f in os.walk(os.curdir):
        if r == "." or "venv" in r or ".idea" in r:
            continue
        for file in f:
            try:
                location = f"{r}\\{file}"
                with open(location, "rb") as r_stream:
                    encrypted = r_stream.read()
                with open(location, "wb") as w_stream:
                    w_stream.write(key.decrypt(encrypted))

                os.rename(location, f"{r}\\{key.decrypt(file).decode('utf-8')}")
            except (binascii.Error, cryptography.fernet.InvalidToken):
                with open(f"{r}\\{file}", "wb") as w_stream:
                    w_stream.write(encrypted)

                print(f"Could not decrypt at '{r}\\{file}'.")
                all_succeed = False

    return all_succeed


def new_key():
    print(f"Your new key is: {Fernet.generate_key().decode('utf-8')}")


main()
