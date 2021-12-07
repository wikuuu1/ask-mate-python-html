from flask import Flask, render_template, request, redirect, url_for
import data_manager
from data_manager import ASCENDING, DESCENDING

app = Flask(__name__)
display_dict = {}

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
    display_dict[question_id] += 1
    pass


@app.route("/add-question")
def route_ask_question():
    pass


if __name__ == "__main__":
    app.run()
