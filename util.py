def date_to_int(date):
    converted_date = ""
    for index, i in enumerate(date):
        if index < 19:
            converted_date += i

    return converted_date
