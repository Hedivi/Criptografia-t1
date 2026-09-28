import os
import math
import time

from .utils import make_sub_table
from .files import read_file, read_bin_file, write_file, write_bin_file

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

BLOCK_SIZE = 256

def make_decipher_table(cipher_text, rows, cols, size):

    k = 0
    table = [[None] * cols for _ in range(rows)]

    for diagonal in range(rows + cols - 1):

        row_start = max(0, diagonal - cols + 1)
        row_end = min(rows - 1, diagonal)

        for row in range(row_start, row_end + 1):
            col = diagonal - row

            index = row * cols + col
            if index < size:
                table[row][col] = cipher_text[k]
                k += 1

    return table


def read_decipher_table(table, rows, cols):

    cipher_text = ""

    for row in range(rows):
        for col in range(cols):
            if table[row][col] is not None:
                cipher_text += table[row][col]

    return cipher_text


def substitution_decipher(cipher_text, sub_table):

    text = []
    for letter in cipher_text:
        index = sub_table.index(letter)
        text.append(chr(ord('A') + index))

    return "".join(text)


def proposed_decipher(args):

    cipher_text = read_file(args.cipher_text)

    key = read_file(args.key)

    size = len(cipher_text)

    cols = len(key)
    rows = math.ceil(size / cols)

    start = time.perf_counter()

    table = make_decipher_table(cipher_text, rows, cols, size)

    cipher_text = read_decipher_table(table, rows, cols)

    sub_table = make_sub_table(key)

    open_text = substitution_decipher(cipher_text, sub_table)

    end = time.perf_counter()

    write_file(args.open_text, open_text)

    return end - start


def aes_decipher(args):

    cipher_text = read_bin_file(args.cipher_text)
    nonce = read_bin_file("nonce-aes.txt")

    key = read_file(args.key)
    key = bytes.fromhex(key)

    aes = AESGCM(key)

    start = time.perf_counter()

    open_text = aes.decrypt(nonce, cipher_text, None)

    end = time.perf_counter()

    write_bin_file(args.open_text, open_text)

    return end - start


def rsa_decipher(args):

    cipher_text = read_bin_file(args.cipher_text)

    private_key_string = read_bin_file(args.key)
        
    private_key = serialization.load_pem_private_key(private_key_string, password=None)

    start = time.perf_counter()

    cipher_blocks = [
        cipher_text[i:i + BLOCK_SIZE]
        for i in range(0, len(cipher_text), BLOCK_SIZE)
    ]

    open_blocks = []

    for block in cipher_blocks:

        open_block = private_key.decrypt(
            block,
            padding.OAEP(
                mgf=padding.MGF1(
                    algorithm=hashes.SHA256()
                ),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        open_blocks.append(open_block)


    open_text = b"".join(open_blocks)

    end = time.perf_counter()

    write_bin_file(args.open_text, open_text)

    return end - start
