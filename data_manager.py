import connection
import database_common
from datetime import datetime
from psycopg2 import sql
from psycopg2.extras import DictCursor

QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@database_common.connection_handler
def get_all_questions_sorted(cursor: DictCursor, order_by: str, order_dir: str) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY {} {}
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


@database_common.connection_handler
def get_selected_question(cursor, question_id: str) -> list:
    query = """
            SELECT *
            FROM question
            WHERE id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answers_for_question(cursor, question_id: str) -> list:
    query = """
            SELECT *
            FROM answer
            WHERE question_id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def save_question_to_table(cursor, new_table_row: list):
    query = """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
            """
    cursor.execute(query, {'submission_time': new_table_row[0], 'view_number': new_table_row[1],
                           'vote_number': new_table_row[2], 'title': new_table_row[3],
                           'message': new_table_row[4], 'image': new_table_row[5]})


@database_common.connection_handler
def get_question_id_by_data(cursor, table_row: list):
    query = """
                SELECT id
                FROM question
                WHERE submission_time=%(submission_time)s AND view_number=%(view_number)s 
                AND vote_number=%(vote_number)s AND title=%(title)s 
                AND message=%(message)s AND image=%(image)s
                """
    cursor.execute(query, {'submission_time': table_row[0], 'view_number': table_row[1],
                           'vote_number': table_row[2], 'title': table_row[3],
                           'message': table_row[4], 'image': table_row[5]})
    return cursor.fetchone()


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
