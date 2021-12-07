import csv
import os

import util
import time

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
                if record_dict[label] == record_dict['id']:
                    values_row.append(util.generate_id())
                if record_dict[label] == record_dict['submission_time']:
                    values_row.append(int(time.time()))
                if record_dict[label] == record_dict['view_number']:
                    values_row.append(1)  # TODO: COUNTER
                if record_dict[label] == record_dict['vote_number']:
                    values_row.append(1)  # TODO: COUNTER-vote_number
                if record_dict[label] == record_dict['title']:
                    values_row.append('')  # TODO: TITLE
                if record_dict[label] == record_dict['message']:
                    values_row.append('')  # TODO: MESSAGE
                if record_dict[label] == record_dict['image']:
                    values_row.append('')  # TODO: IMAGE

                # values_row.append(record_dict[label])
            row = separator.join(values_row)
            file.write(row + "\n")
