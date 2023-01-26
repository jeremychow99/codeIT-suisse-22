import logging
import json

from flask import request, jsonify, Response
from codeitsuisse import app
logger = logging.getLogger(__name__)

app.route('/quordleKeyboard', methods=['POST'])
def quordleKeyboard():
    data = request.get_json()
    answers = data.get("answers")
    numbers = data.get("numbers")
    attempts = data.get("attempts")
    logging.info("data sent for evaluation {}".format(data))
    result, leftovers = grey_letters(answers, attempts)
    str_result = convert_binary(numbers, result, leftovers)
    result = {"part1": result, "part2": str_result}
    logging.info("My result :{}".format(result))
    return jsonify(result)


def grey_letters(answers, attempts):
    alphabet_dict = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9,
        "K": 10,
        "L": 11,
        "M": 12,
        "N": 13,
        "O": 14,
        "P": 15,
        "Q": 16,
        "R": 17,
        "S": 18,
        "T": 19,
        "U": 20,
        "V": 21,
        "W": 22,
        "X": 23,
        "Y": 24,
        "Z": 25,
    }

    number_dict = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H",
        8: "I",
        9: "J",
        10: "K",
        11: "L",
        12: "M",
        13: "N",
        14: "O",
        15: "P",
        16: "Q",
        17: "R",
        18: "S",
        19: "T",
        20: "U",
        21: "V",
        22: "W",
        23: "X",
        24: "Y",
        25: "Z",
    }

    res_list = [""] * 26

    n_attempts = len(attempts)

    for attempt in attempts:

        # Check if attempt corresponds to answer
        if attempt in answers:
            answers.remove(attempt)

        ans_str = "".join(answers)
        for char in attempt:
            if char not in ans_str:
                if res_list[alphabet_dict[char]] == "":
                    res_list[alphabet_dict[char]] = str(n_attempts)

        n_attempts -= 1

    leftover = ""

    for index, result in enumerate(res_list):
        if result == "":
            leftover += number_dict[index]

    res = "".join(res_list)

    return res, leftover


def convert_binary(numbers, result, leftover):

    number_dict = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H",
        8: "I",
        9: "J",
        10: "K",
        11: "L",
        12: "M",
        13: "N",
        14: "O",
        15: "P",
        16: "Q",
        17: "R",
        18: "S",
        19: "T",
        20: "U",
        21: "V",
        22: "W",
        23: "X",
        24: "Y",
        25: "Z",
    }

    str_res = str(result)
    bin_result = []
    res = ""

    bin_str = ""
    for num in numbers:
        if str(num) in str_res:
            bin_str += "1"

        else:
            bin_str += "0"

        if len(bin_str) == 5:
            bin_result.append(bin_str)
            bin_str = ""

    for binary in bin_result:
        res += number_dict[int(binary, 2) - 1]

    return res + leftover