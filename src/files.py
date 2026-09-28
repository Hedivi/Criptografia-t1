import string
import unicodedata

def read_file(filename):

    with open(filename, 'r') as file:
        text = file.read().upper()

    text = text.replace(' ', '').replace('\n', '')

    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.translate(str.maketrans("", "", string.punctuation))

    return text


def read_bin_file(filename):

    with open(filename, 'rb') as file:
        text = file.read()

    return text


def append_file (filename, text):

    with open(filename, 'a') as file:
        file.write(text)


def write_file(filename, text):

    with open(filename, 'w') as file:
        file.write("".join(text))


def write_bin_file (filename, text):

    with open(filename, 'wb') as file:
        file.write(text)


def write_csv(filename, args, time):

    text = ''

    if args.cipher:
        text += "Cifra" + ';'
    else:
        text += "Decifra" + ';'

    text += args.type + ';'

    if args.cipher:
        text += args.open_text + ';'
    else:
        text += args.cipher_text + ';'

    text += str(time)

    text += '\n'

    with open(filename, 'a') as file:
        file.write(text)