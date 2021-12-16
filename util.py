from datetime import datetime


def date_to_int(date):
    converted_date = ""
    for index, i in enumerate(date):
        if index < 19:
            converted_date += i

    return converted_date


def get_actual_date():
    actual_time = datetime.now()
    submission_time = date_to_int(str(actual_time))
    return submission_time
