import csv
import os
import random

QUESTION_DATA_FILE_PATH = 'sample_data/question.csv'
ANSWER_DATA_FILE_PATH = 'sample_data/answer.csv'
QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data_from_file(file_name, separator='#'):
    if file_name == QUESTION_DATA_FILE_PATH:
        headers = QUESTION_DATA_HEADER
    else:
        headers = ANSWER_DATA_HEADER

    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

        data = []
        for element in lines:
            elements_list = element.replace("\n", "").split(separator)
            element_dict = {}
            for i, label in enumerate(headers):
                element_dict[label] = elements_list[i]

            data.append(element_dict)
        return data

    except IOError:
        return []


def write_table_to_file(table, file_name, separator='#'):
    if file_name == QUESTION_DATA_FILE_PATH:
        headers = QUESTION_DATA_HEADER
    else:
        headers = ANSWER_DATA_HEADER

    with open(file_name, "w") as file:
        for record_dict in table:
            values_row = []
            for label in headers:
                values_row.append(record_dict[label])
            row = separator.join(values_row)
            file.write(row + "\n")


def write_data_row_to_file(table, file_name, separator='#'): # TODO: enter zamienic na znak
    if file_name == QUESTION_DATA_FILE_PATH:
        headers = QUESTION_DATA_HEADER
    else:
        headers = ANSWER_DATA_HEADER

    with open(file_name, "a") as file:
        record_dict = table
        values_row = []
        for label in headers:
            values_row.append(record_dict[label])
        row = separator.join(values_row)
        file.write(row + "\n")