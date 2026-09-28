def make_sub_table(key):

    sub_table = key + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    return "".join(dict.fromkeys(sub_table))