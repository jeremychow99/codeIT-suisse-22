import logging
import json
import re

from flask import request, jsonify, Response
from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/tickerStreamPart1', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("stream")
    result = tickerFunc(inputValue)
    logging.info("My result :{}".format(result))
    result = {"output": result}
    return json.dumps(result)


def tickerFunc(stream):
    res_list = []
    time_dict = dict()  # Tickers based on timestamp (For handling different trades)

    for trade in stream:
        trade_list = trade.split(",")
        time_stamp = trade_list[0]

        if time_stamp not in time_dict:
            time_dict[time_stamp] = dict()

        # Tabulate quantity and notional price
        for i in range(1, len(trade_list), 3):
            quantity = int(trade_list[i + 1])
            price = float(trade_list[i + 2])
            notional = quantity * price

            if trade_list[i] in time_dict[time_stamp]:
                time_dict[time_stamp][trade_list[i]][0] += quantity
                time_dict[time_stamp][trade_list[i]][1] += notional

            else:
                time_dict[time_stamp][trade_list[i]] = [quantity, notional]

    # Convert dict to list
    ticker_list = []

    for timestamp, value in time_dict.items():
        for ticker, data in value.items():
            ticker_str = ",".join([ticker, str(data[0]), str(round(data[1], 1))])
            ticker_list.append(ticker_str)

        # Sort list
        ticker_list.sort()
        result = ",".join(ticker_list)
        res_list.append(f"{timestamp},{result}")

    res_list.sort()

    return res_list


def cumulate_ticker(trade_list):
    time_stamp = trade_list[0]
    ticker_dict = dict()

    # Tabulate quantity and notional price
    for i in range(1, len(trade_list), 3):
        quantity = int(trade_list[i + 1])
        price = float(trade_list[i + 2])
        notional = quantity * price

        if trade_list[i] in ticker_dict:
            ticker_dict[trade_list[i]][0] += quantity
            ticker_dict[trade_list[i]][1] += notional

        else:
            ticker_dict[trade_list[i]] = [quantity, notional]

    # Convert dict to list
    res_list = []

    for key, value in ticker_dict.items():
        ticker_str = ",".join([key, str(value[0]), str(round(value[1], 1))])
        res_list.append(ticker_str)

    # Sort list
    res_list.sort()

    result = ",".join(res_list)

    return time_stamp + "," + result


@app.route('/tickerStreamPart2', methods=['POST'])
def ticker2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    quantityBlock = data.get("quantityBlock")
    result = to_cumulative_delayed(stream, quantityBlock)
    logging.info("My result :{}".format(result))
    result = {"output": result}
    return json.dumps(result)


def to_cumulative_delayed(stream, quantity_block):
    stream.sort()
    track_dict = {}
    result = []

    for trade in stream:
        order_list = trade.split(",")
        timestamp = order_list[0]
        block_list = (
            []
        )  # Store all ticker that hits the quantity blocks during this timestamp

        for i in range(1, len(order_list), 3):
            curr_qty = int(order_list[i + 1])
            price = float(order_list[i + 2])

            # Ticker and quantity exist
            if order_list[i] in track_dict:
                exist_qty, exist_notional = track_dict[order_list[i]]

                # Check quantity match the quantity block
                if quantity_block <= exist_qty + curr_qty:

                    required_qty = quantity_block - exist_qty
                    notional = required_qty * price

                    # Current trade and existing quantity exceeds quantity block (Splitting required)
                    if curr_qty > required_qty:
                        excess_qty = curr_qty - required_qty

                        block_list.append(
                            f"{order_list[i]},{quantity_block},{notional + exist_notional}"
                        )

                        # Store leftover quantity and notional back into tracking dictionary
                        track_dict[order_list[i]] = [excess_qty, excess_qty * price]

                    # Current trade quantity = required quantity
                    else:
                        block_list.append(
                            f"{order_list[i]},{quantity_block},{notional + exist_notional}"
                        )
                        track_dict[order_list[i]] = [0, 0]

                else:
                    track_dict[order_list[i]][0] += curr_qty
                    track_dict[order_list[i]][1] += curr_qty * price

            else:
                if curr_qty == quantity_block:
                    block_list.append(
                        f"{order_list[i]},{quantity_block},{curr_qty * price}"
                    )

                else:
                    track_dict[order_list[i]] = [curr_qty, curr_qty * price]

        # Check if any quantity blocks fulfilled in current timestamp
        if block_list:
            # Sort quantity blocks by ticker alphabetical order
            block_list.sort()
            result.append(f"{timestamp},{','.join(block_list)}")

    return result





