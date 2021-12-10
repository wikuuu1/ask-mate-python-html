from flask import Flask, render_template, request, redirect
import data_manager
import connection
from data_manager import ASCENDING, DESCENDING
import time
import util

app = Flask(__name__)

ORDER_DIRECTION = 'order_direction'
ORDER_DIRECTIONS = {ASCENDING: 'Ascending', DESCENDING: 'Descending'}

ORDER_BY = 'order_by'
SORTING_MODES = {'submission_time': 'Time added',
                 'view_number': 'Views',
                 'vote_number': 'Votes',
                 'title': 'Title',
                 'message': 'Message'}


@app.route("/")
@app.route("/list")
def list_questions():
    users_questions = data_manager.get_all_questions()
    headers_list = data_manager.get_questions_headers()

    order_by = request.args.get(ORDER_BY, 'submission_time')
    order_direction = request.args.get(ORDER_DIRECTION, DESCENDING)

    questions_sorted = data_manager.sort_data(users_questions, order_direction, order_by)
    print(questions_sorted)
    questions_converted = data_manager.convert_timestamp_to_date_in_data(questions_sorted)

    return render_template('list.html',
                           questions=questions_converted,
                           headers=headers_list,
                           sorting_modes=SORTING_MODES,
                           sorting_direction=ORDER_DIRECTIONS,
                           current_ordering=order_by,
                           current_direction=order_direction)


@app.route("/question/<question_id>")
def route_display_question(question_id):
    users_questions = data_manager.get_all_questions()
    # headers_list = data_manager.get_questions_headers()
    table = util.increase_view_number(users_questions, question_id)
    connection.write_table_to_file(table, connection.QUESTION_DATA_FILE_PATH)
    questions_converted = data_manager.convert_timestamp_to_date_in_data(users_questions)
    question_to_display = util.find_question_in_dictionary(questions_converted, question_id)

    return render_template('display_question.html',
                           question=question_to_display)


# @app.route("/question/<question_id>/delete")
# def route_display_question(question_id):
#
#     return redirect("/")


@app.route("/add-question", methods=["POST"])
def route_create_new_question():
    unique_id = str(util.generate_id())
    submission_time_unix_format = str(int(time.time()))
    question_title = request.form['new_question']
    question_description = request.form['question_description']
    table = {'id': unique_id, 'submission_time': submission_time_unix_format, 'view_number': '0',
             'vote_number': '0', 'title': question_title,
             'message': question_description, 'image': 'image'}
    connection.write_data_row_to_file(table, connection.QUESTION_DATA_FILE_PATH)
    return redirect("/")


@app.route("/add-question", methods=["GET"])
def route_ask_question():
    return render_template('add_question.html')


if __name__ == "__main__":
    app.run(debug=True)
