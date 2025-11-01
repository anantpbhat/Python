"""Class to decrypt a Bin file with provided AES key."""

import sys
from Crypto.Cipher import AES


class Decrypt():
    """Decrypt Class that could be imported from any python script"""
    def do_decrypt(self, datfile, aes_key):
        """Function to decrypt passwords in a binfile"""
        with open(datfile, "rb") as fl:
            tag = fl.read(16)
            nonce = fl.read(15)
            ciphertext = fl.read()
        cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)
        try:
            Scrt = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            print("Somehow the Binfile is not the same or Bad AES Key!!")
            sys.exit(1)
        return Scrt.decode()