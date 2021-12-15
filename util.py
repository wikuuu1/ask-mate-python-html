import hashlib


def generate_id(data):
    data_as_list = list(data.listvalues())
    string_sum = ""
    for element in data_as_list:
        string_sum += element[0]
    md5_hash = hashlib.md5()
    md5_hash.update(string_sum.encode())

    return md5_hash.hexdigest()


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


def delete_question(table, id):
    dictionary_to_remove = 0
    for index, dictionary in enumerate(table):
        if dictionary['id'] == id:
            dictionary_to_remove = dictionary
    table.remove(dictionary_to_remove)
    return table


def edit_question(table, id, title, message):
    for dictionary in table:
        if dictionary['id'] == id:
            dictionary['title'] = title
            dictionary['message'] = message
    return table


def find_answers_for_question(table, id):
    list_for_answers = []
    for dictionary in table:
        if dictionary['question_id'] == id:
            list_for_answers.append(dictionary)
    return list_for_answers


def date_to_int(date):
    converted_date = ""
    for index, i in enumerate(date):
        if index < 19:
            converted_date += i

    return converted_date
