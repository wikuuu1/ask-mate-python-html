import connection
import database_common
from datetime import datetime
from psycopg2 import sql
from psycopg2.extras import DictCursor

QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_questions_headers():
    return QUESTION_DATA_HEADER


def get_answers_headers():
    return ANSWER_DATA_HEADER


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
def get_question_by_id(cursor, question_id: str) -> list:
    query = """
            SELECT *
            FROM question
            WHERE id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def update_view_number(cursor, question_id: str):
    query = """
            UPDATE question
            SET view_number=view_number + 1
            WHERE id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


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


@database_common.connection_handler
def save_answer_to_table(cursor, new_table_row: list):
    query = """
                INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
                """
    cursor.execute(query, {'submission_time': new_table_row[0], 'vote_number': new_table_row[1],
                           'question_id': new_table_row[2], 'message': new_table_row[3],
                           'image': new_table_row[4]})


@database_common.connection_handler
def delete_question_in_file(cursor, question_id):
    query = """
                DELETE FROM question
                WHERE id=%(question_id)s
                """
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def edit_question(cursor, question_id, title, message):
    query = """
                UPDATE question
                SET title=%(title)s, message=%(message)s
                WHERE id=%(question_id)s 
                """
    cursor.execute(query, {'question_id': question_id, 'title': title, 'message': message})


@database_common.connection_handler
def save_comment_to_table(cursor, new_table_row: list):
    query = """
            INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
            VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
            """
    cursor.execute(query, {'question_id': new_table_row[0], 'answer_id': new_table_row[1],
                           'message': new_table_row[2], 'submission_time': new_table_row[3],
                           'edited_count': new_table_row[4]})


@database_common.connection_handler
def delete_answer_in_database(cursor, answer_id):
    query = """
                DELETE FROM answer
                WHERE id=%(answer_id)s
                """
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id: str) -> list:
    query = """
            SELECT *
            FROM answer
            WHERE id=%(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_comments_for_question(cursor, question_id: str) -> list:
    query = """
            SELECT *
            FROM comment
            WHERE question_id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()
