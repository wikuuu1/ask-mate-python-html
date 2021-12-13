import connection
import database_common
from datetime import datetime
from psycopg2 import sql
from psycopg2.extras import DictCursor

QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@database_common.connection_handler
def get_all_questions(cursor: DictCursor, order_by: str, order_dir: str) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY {0}
        {1}
        """.format(order_by, order_dir)

    cursor.execute(query, {'order_by': order_by, 'order_dir': order_dir})

    return cursor.fetchall()


@database_common.connection_handler
def get_all_answers(cursor: DictCursor) -> list:
    query = """
        SELECT *
        FROM answer"""
    cursor.execute(query)

    return cursor.fetchall()


def write_answer_to_file(new_data_row):
    return connection.write_data_row_to_file(new_data_row, connection.ANSWER_DATA_FILE_PATH)


def write_question_to_file(table):
    return connection.write_data_row_to_file(table, connection.QUESTION_DATA_FILE_PATH)


def overwrite_question_in_file(table):
    return connection.write_table_to_file(table, connection.QUESTION_DATA_FILE_PATH)


def convert_timestamp_to_date_in_data(data):
    for row in data:
        timestamp = int(row['submission_time'])
        date = datetime.fromtimestamp(timestamp)
        row['submission_time'] = date
    return data


def get_questions_headers():
    return QUESTION_DATA_HEADER


def get_answers_headers():
    return ANSWER_DATA_HEADER
