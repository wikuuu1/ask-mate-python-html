from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection

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


@app.route("/add-question", methods=["GET", "POST"])
def route_ask_question():
    #TODO: ALL TO CHECK, FIND THE BUG
    if request.method == "POST":
        users_questions = data_manager.get_all_questions()
        headers_list = data_manager.get_questions_headers()

        new_question = {}
        for header in headers_list:
            new_question[header] = request.form[header]

        users_questions.append(new_question)
        connection.write_table_to_file(users_questions, 'question.csv')
        return redirect("/")

    return render_template('add_question.html')


if __name__ == "__main__":
    app.run(debug=True)
