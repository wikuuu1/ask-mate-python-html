import connection
from datetime import datetime

ASCENDING = "ascending"
DESCENDING = "descending"


def get_all_questions():
    return connection.get_all_data_from_file(connection.QUESTION_DATA_FILE_PATH)


def get_all_answers():
    return connection.get_all_data_from_file(connection.ANSWER_DATA_FILE_PATH)


def write_answer_to_file(new_data_row):
    return connection.write_data_row_to_file(new_data_row, connection.ANSWER_DATA_FILE_PATH)


def write_question_to_file(table):
    return connection.write_data_row_to_file(table, connection.QUESTION_DATA_FILE_PATH)


def overwrite_question_in_file(table):
    return connection.write_table_to_file(table, connection.QUESTION_DATA_FILE_PATH)


def sort_data(data, direction, ordering_key):
    for _ in range(len(data)):
        for i, _ in enumerate(range(len(data)-1)):
            if ordering_key not in ['submission_time','view_number', 'vote_number']:
                if direction == DESCENDING and data[i][ordering_key] < data[i+1][ordering_key]:
                    data[i], data[i+1] = data[i+1], data[i]
                elif direction == ASCENDING and data[i][ordering_key] > data[i+1][ordering_key]:
                    data[i], data[i+1] = data[i+1], data[i]
            else:
                if direction == DESCENDING and int(data[i][ordering_key]) < int(data[i+1][ordering_key]):
                    data[i], data[i+1] = data[i+1], data[i]
                elif direction == ASCENDING and int(data[i][ordering_key]) > int(data[i+1][ordering_key]):
                    data[i], data[i+1] = data[i+1], data[i]
    return data


def convert_timestamp_to_date_in_data(data):
    for row in data:
        timestamp = int(row['submission_time'])
        date = datetime.fromtimestamp(timestamp)
        row['submission_time'] = date
    return data


def get_questions_headers():
    return connection.QUESTION_DATA_HEADER
