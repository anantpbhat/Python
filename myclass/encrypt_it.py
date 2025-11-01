"""Class to encrypt an input string in to a Bin file and an AES key"""

from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Encrypt():
    """Class to Encrypt plaintext password from cmdline input"""
    def do_encrypt(self):
        """Function prompts for password input and returns encrypted binfile and a key"""
        SCRT = getpass("Please enter your password here: ", stream=None).rstrip
        SCRT = SCRT.encode()
        aes_key = get_random_bytes(16)
        cipher = AES.new(aes_key, AES.MODE_OCB)
        ciphertext, tag = cipher.encrypt_and_digest(SCRT)
        assert len(cipher.nonce) == 15
        binfile = "bin/secret.bin"
        with open(binfile, "wb") as fl:
            fl.write(tag)
            fl.write(cipher.nonce)
            fl.write(ciphertext)
        print(f"Encrypted Binfile created - {binfile}")
        print(f"Note this Key: {aes_key}")
