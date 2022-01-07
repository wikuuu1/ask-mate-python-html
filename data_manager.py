import database_common
from psycopg2.extras import RealDictCursor, RealDictRow


@database_common.connection_handler
def get_all_questions_sorted(cursor: RealDictCursor, order_by: str, order_dir: str) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY {} {}
        """.format(order_by, order_dir)

    cursor.execute(query)

    return cursor.fetchall()


@database_common.connection_handler
def get_all_answers(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer"""
    cursor.execute(query)

    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id: int) -> RealDictRow:
    query = """
            SELECT *
            FROM question
            WHERE id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def update_view_number(cursor: RealDictCursor, question_id: int):
    query = """
            UPDATE question
            SET view_number=view_number + 1
            WHERE id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def get_answers_for_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
            SELECT *
            FROM answer
            WHERE question_id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def save_question_to_table(cursor: RealDictCursor, new_table_row: list) -> int:
    query = """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
            """
    cursor.execute(query, {'submission_time': new_table_row[0], 'view_number': new_table_row[1],
                           'vote_number': new_table_row[2], 'title': new_table_row[3],
                           'message': new_table_row[4], 'image': new_table_row[5]})
    cursor.execute("SELECT lastval()")
    return cursor.fetchone()["lastval"]


@database_common.connection_handler
def save_answer_to_table(cursor: RealDictCursor, new_table_row: list):
    query = """
                INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
                """
    cursor.execute(query, {'submission_time': new_table_row[0], 'vote_number': new_table_row[1],
                           'question_id': new_table_row[2], 'message': new_table_row[3],
                           'image': new_table_row[4]})


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int):
    query = """
                DELETE FROM question
                WHERE id=%(question_id)s
                """
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def edit_question(cursor: RealDictCursor, question_id: int, title: str, message: str, image: str):
    if not image:
        query = """
                    UPDATE question
                    SET title=%(title)s, message=%(message)s
                    WHERE id=%(question_id)s 
                    """
        cursor.execute(query, {'question_id': question_id, 'title': title, 'message': message})
    else:
        query = """
                    UPDATE question
                    SET title=%(title)s, message=%(message)s, image=%(image)s
                    WHERE id=%(question_id)s 
                    """
        cursor.execute(query, {'question_id': question_id, 'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def save_comment_to_table(cursor: RealDictCursor, new_table_row: list):
    query = """
            INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
            VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
            """
    cursor.execute(query, {'question_id': new_table_row[0], 'answer_id': new_table_row[1],
                           'message': new_table_row[2], 'submission_time': new_table_row[3],
                           'edited_count': new_table_row[4]})


@database_common.connection_handler
def get_comments_for_answer(cursor, answer_id: str):
    query = """
                SELECT *
                FROM comment
                WHERE answer_id=%(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_answer_in_database(cursor: RealDictCursor, answer_id: int):
    query = """
                DELETE FROM answer
                WHERE id=%(answer_id)s
                """
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def delete_comment_in_database(cursor: RealDictCursor, comment_id: int):
    query = """
                DELETE FROM comment
                WHERE id=%(comment_id)s
                """
    cursor.execute(query, {'comment_id': comment_id})


@database_common.connection_handler
def edit_answer(cursor: RealDictCursor, answer_id: int, message: str, image: str) -> RealDictRow:
    if image:
        query = """
                    UPDATE answer
                    SET message=%(message)s, image=%(image)s
                    WHERE id=%(answer_id)s;
                    SELECT question_id
                    FROM answer
                    WHERE id=%(answer_id)s
                    """
        cursor.execute(query, {'answer_id': answer_id, 'message': message, 'image': image})

    else:
        query = """
                    UPDATE answer
                    SET message=%(message)s
                    WHERE id=%(answer_id)s;
                    SELECT question_id
                    FROM answer
                    WHERE id=%(answer_id)s
                    """
        cursor.execute(query, {'answer_id': answer_id, 'message': message})

    return cursor.fetchone()['question_id']


@database_common.connection_handler
def edit_comment_in_database(cursor: RealDictCursor, comment_id: int, message: str) -> int:
    query = """
                UPDATE comment
                SET message=%(message)s
                WHERE id=%(comment_id)s;
                SELECT question_id
                FROM comment
                WHERE id=%(comment_id)s;
                """
    cursor.execute(query, {'comment_id': comment_id, 'message': message})
    return cursor.fetchone()['question_id']


@database_common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, answer_id: str) -> RealDictRow:
    query = """
            SELECT *
            FROM answer
            WHERE id=%(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, comment_id: str) -> RealDictRow:
    query = """
            SELECT *
            FROM comment
            WHERE id=%(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_comments_for_question(cursor: RealDictCursor, question_id: str) -> list:
    query = """
            SELECT *
            FROM comment
            WHERE question_id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def update_question_vote_number(cursor: RealDictCursor, question_id: str, vote_dir: str):
    query = """
            UPDATE answer
            SET vote_number=vote_number {} 1   
            WHERE id=%(question_id)s""".format(vote_dir)
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def update_answer_vote_number(cursor: RealDictCursor, answer_id: str, vote_dir: str):
    query = """
            UPDATE answer
            SET vote_number=vote_number {} 1   
            WHERE id=%(answer_id)s""".format(vote_dir)
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def get_question_id_by_answer_id(cursor: RealDictCursor, answer_id: str) -> RealDictRow:
    query = """
            SELECT question_id
            FROM answer
            WHERE id=%(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def delete_answers_to_questions(cursor: RealDictCursor, question_id: str):
    query = """
                DELETE FROM answer
                WHERE quesiton_id=%(question_id)s
                """
    cursor.execute(query, {'question_id': question_id})
