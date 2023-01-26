import logging
import json

from flask import request, jsonify, Response
from codeitsuisse import app
logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = generate_max(data)
    logging.info("My result :{}".format(result))
    return jsonify(result)
    # result = json.dumps(result)
    # return result


def find_max(price, max_dict, max_price=0):

    if price in max_dict:
        return int(max(max_price, max_dict[price]))

    if price % 2 == 0:
        new_price = price / 2
        return find_max(new_price, max_dict, max_price)

    if price % 2 != 0:
        new_price = price * 3 + 1
        max_price = max(new_price, max_price)
        return find_max(new_price, max_dict, max_price)


def generate_max(price_lists):
    res = []

    max_dict = {1: 4}

    for price_list in price_lists:
        max_price_list = []
        logging.info(f"test case: {price_list}")

        for price in price_list:

            if price in max_dict:
                max_price = max_dict[price]

            else:
                max_price = max(find_max(price, max_dict), price)
                max_dict[price] = max_price

            max_price_list.append(max_price)

        res.append(max_price_list)
    return res