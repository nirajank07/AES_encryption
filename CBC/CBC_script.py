#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        self.key = key


    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'CBC_script.py'):  # name of the file to be put here
                    dirs.append(dirName + "//" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = b'[EX\xa5\x55\xf3I{\x45$\x55(\x7b\xbb\xbf\xc0\x85)\x10nc\x94\xc3)j\xdf\xcb\xc4\x94\x34(\xd2'
enc = Encryptor(key)
clear = lambda: os.system('cls')


def main():
    while True:
        clear()
        choice = int(input(
            " Select an option: \n1 -> Encrypt single file\n2 -> Decrypt single file\n3 -> Encrypt all files in the curr folder\n4 -> Decrypt all files in the curr folder\n5 -> Quit\n"))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("Enter the name of the file to encrypt: ")))
        elif choice == 2:
            enc.decrypt_file(str(input("Enter the name of the file to decrypt: ")))
        elif choice == 3:
            start = time.time()
            enc.encrypt_all_files()
            end = time.time()
            print("Took " + str(end - start) + " seconds to encrypt!")
        elif choice == 4:
            start = time.time()
            enc.decrypt_all_files()
            end = time.time()
            print("Took " + str(end - start) + " seconds to decrypt!")
        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")

if __name__ == "__main__":
    main()
