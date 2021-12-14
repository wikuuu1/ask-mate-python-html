from flask import Flask, render_template, request, redirect
import data_manager
import connection
import time
import util

app = Flask(__name__)

ORDER_BY = 'order_by'
ORDER_BY_LABELS = {'submission_time': 'Time added',
                   'view_number': 'Views',
                   'vote_number': 'Votes',
                   'title': 'Title',
                   'message': 'Message'}

ORDER_DIR = 'order_direction'
ORDER_DIR_LABELS = {'ascending': 'Ascending',
                    'descending': 'Descending'}

ORDER_DIR_SQL = {'ascending': 'ASC',
                 'descending': 'DESC'}


@app.route("/")
@app.route("/list")
def list_questions():
    headers_list = data_manager.get_questions_headers()
    order_by = request.args.get(ORDER_BY, 'submission_time')
    order_dir = request.args.get(ORDER_DIR, 'descending')

    if order_by in ORDER_BY_LABELS:
        order_dir_sql = ORDER_DIR_SQL[order_dir]
        users_questions = data_manager.get_all_questions_sorted(order_by, order_dir_sql)

        return render_template('list.html',
                               questions=users_questions,
                               headers=headers_list,
                               order_by_labels=ORDER_BY_LABELS,
                               order_dir_labels=ORDER_DIR_LABELS,
                               current_order_by=order_by,
                               current_order_dir=order_dir)

    return redirect("/")


@app.route("/question/<question_id>")
def route_display_question(question_id):
    selected_question = data_manager.get_selected_question(question_id)
    all_answers = data_manager.get_all_answers()
    users_answer = util.find_answers_for_question(all_answers, question_id)

    return render_template('display_question.html',
                           question=selected_question, users_answer=users_answer, answer_headers=connection.ANSWER_DATA_HEADER)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    users_questions = data_manager.get_all_questions_sorted()
    question_to_delete = util.delete_question(users_questions, question_id)
    data_manager.overwrite_question_in_file(question_to_delete)

    return redirect("/")


@app.route("/question/<question_id>/edit", methods=["POST"])
def edit_question(question_id):
    users_questions = data_manager.get_all_questions_sorted()
    title = request.form['edited_question']
    message = request.form['edited_description']
    table = util.edit_question(users_questions, question_id, title, message)
    data_manager.overwrite_question_in_file(table)

    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/edit", methods=["GET"])
def get_edit_question(question_id):
    users_questions = data_manager.get_all_questions_sorted()
    question_to_edit = util.find_question_in_dictionary(users_questions, question_id)
    return render_template('edit_question.html', question=question_to_edit)


@app.route("/add-question", methods=["POST"])
def route_create_new_question():
    unique_id = str(util.generate_id())
    submission_time_unix_format = str(int(time.time()))
    question_title = request.form['new_question']
    question_description = request.form['question_description']
    table = {'id': unique_id, 'submission_time': submission_time_unix_format, 'view_number': '0',
             'vote_number': '0', 'title': question_title,
             'message': question_description, 'image': 'image'}
    data_manager.write_question_to_file(table)
    return redirect(f'/question/{unique_id}')


@app.route("/add-question", methods=["GET"])
def route_ask_question():
    return render_template('add_question.html')


@app.route("/question/<question_id>/new-answer", methods=["POST"])
def route_new_answer(question_id):
    answer_id = str(util.generate_id())
    timestamp = str(int(time.time()))
    answer = request.form['answer_description']
    image = "image"
    new_data_row = {"id": answer_id, 'submission_time': timestamp, 'vote_number': '0', 'question_id': question_id,
                    'message': answer, 'image': image}
    data_manager.write_answer_to_file(new_data_row)

    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/new-answer", methods=["GET"])
def get_new_answer(question_id):
    users_answer = data_manager.get_all_answers()
    users_questions = data_manager.get_all_questions_sorted()
    question_to_answer = util.find_question_in_dictionary(users_answer, question_id)
    question_to_edit = util.find_question_in_dictionary(users_questions, question_id)
    return render_template('answer.html', answer=question_to_answer, question=question_to_edit)


if __name__ == "__main__":
    app.run(debug=True)
