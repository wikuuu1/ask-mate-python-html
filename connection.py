import ast

QUESTION_DATA_FILE_PATH = 'sample_data/question.csv'
ANSWER_DATA_FILE_PATH = 'sample_data/answer.csv'
QUESTION_DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_DATA_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data_from_file(file_name):
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

        data = []
        for element in lines:
            element.replace("\n", "")
            if len(element) > 0:
                data.append(ast.literal_eval(element))
        return data

    except IOError:
        return []


def write_table_to_file(table, file_name):
    with open(file_name, "w") as file:
        for row in table:
            for key in row:
                row[key] = row[key].encode()
            file.write(str(row) + "\n")


def write_data_row_to_file(row, file_name):
    with open(file_name, "a") as file:
        for key in row:
            print(row[key])
            row[key] = row[key].encode()
            print(row[key])
        file.write(str(row) + "\n")
