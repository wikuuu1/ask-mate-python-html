import random


def generate_id():
    """         number_of_small_letters=4,
                number_of_capital_letters=2,
                number_of_digits=2,
    """
    id_list = []
    for i in range(4):
        id_list.append(chr(random.randint(97, 122)))
    for i in range(2):
        id_list.append(chr(random.randint(65, 90)))
    for i in range(2):
        id_list.append(random.randint(0, 9))
    random.shuffle(id_list)
    new_id = ""
    for i in id_list:
        new_id += str(i)

    return new_id


def find_question_in_dictionary(table, id):
    for dictionary in table:
        if dictionary['id'] == id:
            return dictionary


def increase_view_number(table, id):
    for dictionary in table:
        if dictionary['id'] == id:
            dictionary['view_number'] = int(dictionary['view_number']) + 1
            dictionary['view_number'] = str(dictionary['view_number'])
            return table