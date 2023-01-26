from datetime import date, timedelta
import logging
import json
import re

from flask import request, jsonify, Response
logger = logging.getLogger(__name__)

@app.route('/calendarDays', methods=['POST'])
def calenderDays():
    data = request.get_json()
    numbers = data.get("numbers")
    logging.info("data sent for evaluation {}".format(data))
    part1 = tabulate_year_str(numbers)
    part2 = tabulate_doy(part1)
    my_dict = {"part1": part1, "part2": part2}
    return jsonify(my_dict)


def tabulate_year_str(year_list):
    year = year_list[0]
    day_num_list = year_list[1:]

    # Reference Date
    strt_date = date(int(year), 1, 1)

    year_dict = {
        1: set(),
        2: set(),
        3: set(),
        4: set(),
        5: set(),
        6: set(),
        7: set(),
        8: set(),
        9: set(),
        10: set(),
        11: set(),
        12: set(),
    }

    for day_num in day_num_list:

        if day_num <= 0 or day_num >= 366:
            continue

        else:
            res_date = strt_date + timedelta(days=day_num - 1)

            month = res_date.month
            dayofweek = res_date.weekday()

            year_dict[month].add(dayofweek)

    # Populate Results
    res = ""

    alldays = set([0, 1, 2, 3, 4, 5, 6])
    weekday = set([0, 1, 2, 3, 4])
    weekend = set([5, 6])

    dayofweek = {0: 'm', 1: 't', 2: 'w', 3: 't', 4: 'f', 5: 's', 6: 's'}

    for days in year_dict.values():
        if days == alldays:
            res += "alldays,"
        elif days == weekday:
            res += "weekday,"
        elif days == weekend:
            res += "weekend,"
        else:
            day_list = list(days)

            for key, value in dayofweek.items():
                if key in day_list:
                    res += value
                else:
                    res += " "

            res += ","

    return res


def tabulate_doy(input):
    ws_index = input.index(" ")
    month_list = input.split(",")
    year = 2001 + ws_index

    res = [year]

    for index, days in enumerate(month_list[:-1]):
        strt_date = date(year, index + 1, 1)
        day_of_year = int(strt_date.strftime('%j'))
        day_of_week = strt_date.weekday()

        if days == "alldays":
            res = res + [day_of_year + day_num for day_num in range(7)]

        elif days == "weekday":
            for i in range(7):
                if (day_of_week + i % 7) not in [5, 6]:
                    res.append(day_of_year + i)

        elif days == "weekend":
            for i in range(7):
                if (day_of_week + i % 7) in [5, 6]:
                    res.append(day_of_year + i)

        else:
            for i in range(len(days)):
                if days[i] != " ":
                    # Moving forward
                    if day_of_week <= i:
                        res.append(day_of_year + i - day_of_week)

                    # Have to move forward to following week
                    else:
                        res.append(day_of_year + i + 7 - day_of_week)

    return res