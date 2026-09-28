import argparse

def str_to_bool(value):

    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False


def parse_args():

    parser = argparse.ArgumentParser(
        description="Trabalho de Criptografia 1"
    )

    parser.add_argument(
        "--open_text",
        type=str,
        required=True,
        help="Arquivo com o texto aberto."
    )

    parser.add_argument(
        "--cipher_text",
        type=str,
        required=True,
        help="Arquivo para salvar o texto cifrado."
    )

    parser.add_argument(
        "--cipher",
        type=str_to_bool,
        required=True,
        help="Indica se é para cifrar (TRUE) ou decifrar (FALSE)."
    )

    parser.add_argument(
        "--key",
        type=str,
        required=True,
        help="Arquivo com a chave ou que será salvo/lido a chave no RSA"
    )

    parser.add_argument(
        '--type', 
        type=str, 
        choices=['rsa', 'aes', 'proposed'], 
        required=True,
        help="Algoritmo a ser executado."
    )

    return parser.parse_args()