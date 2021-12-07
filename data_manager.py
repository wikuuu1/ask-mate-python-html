import connection
from datetime import datetime


def get_all_questions():
    return connection.get_all_data_from_file(connection.QUESTION_DATA_FILE_PATH)


def sort_data_by_timestamp(data):
    for _ in range(len(data)):
        for i, _ in enumerate(range(len(data)-1)):
            if data[i]['submission_time'] > data[i+1]['submission_time']:
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
