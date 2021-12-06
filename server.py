from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    users_questions = data_manager.get_all_questions()
    questions_sorted_by_timestamp = data_manager.sort_data_by_timestamp(users_questions)
    questions_timestamp_converted = data_manager.convert_timestamp_to_date_in_data(questions_sorted_by_timestamp)
    headers_list = data_manager.get_questions_headers()

    return render_template('list.html', questions=questions_timestamp_converted, headers=headers_list)

@app.route("/question/<question_id>")
def route_display_question(question_id):
    pass

@app.route("/add-question")
def route_ask_question():
    pass


if __name__ == "__main__":
    app.run()
