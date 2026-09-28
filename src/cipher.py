import os
import math
import time

from .utils import make_sub_table
from .files import read_file, write_file, read_bin_file, write_bin_file

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

BLOCK_SIZE = 190

def substitution_cipher (open_text, sub_table):

    cipher_text = []
    for letter in open_text:
        index = ord(letter) - ord('A')
        cipher_text.append(sub_table[index])

    return "".join(cipher_text)


def create_cipher_table (text, key):

    cols = len(key)

    lines = math.ceil(len(text) / cols)
    matrix = [[None] * cols for _ in range(lines)]

    i = 0
    j = 0
    k = 0

    while k < len(text):
        matrix[i][j] = text[k]
    
        k += 1
        j += 1

        if j >= cols:
            i += 1
            j = 0

    return matrix, lines, cols


def read_cipher_table(table, lines, cols):

    cipher_text = []
    for diagonal in range(lines + cols - 1):

        row_start = max(0, diagonal - cols + 1)
        row_end = min(lines - 1, diagonal)

        for row in range(row_start, row_end + 1):
            col = diagonal - row

            if table[row][col] is not None:
                cipher_text.append(table[row][col])

    return "".join(cipher_text)


def proposed_cipher(args):

    open_text = read_file(args.open_text)
    open_text = open_text.replace(' ', '')

    key = read_file(args.key)

    start = time.perf_counter()

    sub_table = make_sub_table(key)

    cipher_text1 = substitution_cipher(open_text, sub_table)

    matrix, lines, cols = create_cipher_table(cipher_text1, key)

    cipher_text2 = read_cipher_table(matrix, lines, cols)

    end = time.perf_counter()

    write_file(args.cipher_text, cipher_text2)

    return end - start


def aes_cipher(args):

    open_text = read_bin_file(args.open_text)
    nonce = read_bin_file("nonce-aes.txt")

    key = read_file(args.key)
    key = bytes.fromhex(key)

    aes = AESGCM(key)

    start = time.perf_counter()

    cipher_text = aes.encrypt(nonce, open_text, None)

    end = time.perf_counter()

    write_bin_file(args.cipher_text, cipher_text)

    return end - start


def rsa_cipher (args):

    open_text = read_bin_file(args.open_text)

    private_key_pem = read_bin_file(args.key)

    private_key = serialization.load_pem_private_key(private_key_pem, password=None)

    public_key = private_key.public_key()

    start = time.perf_counter()

    blocks = [open_text[i:i + BLOCK_SIZE] for i in range(0, len(open_text), BLOCK_SIZE)]

    cipher_blocks = []
    for block in blocks:
        cipher = public_key.encrypt(block, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label = None))

        cipher_blocks.append(cipher)

    cipher_text = b"".join(cipher_blocks)

    end = time.perf_counter()

    write_bin_file(args.cipher_text, cipher_text)

    return end - start
