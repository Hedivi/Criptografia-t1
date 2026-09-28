from src.argparser import parse_args
from src.cipher import proposed_cipher, rsa_cipher, aes_cipher
from src.decipher import proposed_decipher, rsa_decipher, aes_decipher
from src.files import write_csv

def main():

    args = parse_args()

    if args.cipher == True:

        if args.type == 'rsa':
            time = rsa_cipher(args)

        elif args.type == 'aes':
            time = aes_cipher(args)

        elif args.type == 'proposed':
            time = proposed_cipher(args)

    else:

        if args.type == 'rsa':
            time = rsa_decipher(args)

        elif args.type == 'aes':
            time = aes_decipher(args)

        elif args.type == 'proposed':
            time = proposed_decipher(args)

    write_csv("estatistica.csv", args, time)


if __name__ == "__main__":
    main()
