from random import choice

def gen_id():
    id_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    id_rand = choice(id_list)
    return id_rand