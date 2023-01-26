
@app.route('/magicCauldrons', methods=['POST'])
def magicCauldrons():
    data = request.get_json()
    part1 = data.get("part1")
    time = part1.get("time")
    flow = part1.get("flow_rate")
    row = part1.get("row_number")
    col = part1.get("col_number")
    result = magic(flow, row, col, time)
    result = {"part1": result, "part2": 0, "part3": 0.01, "part4": 0}
    logging.info("data sent for evaluation {}".format(data))
    return jsonify(result)


def magic(flow, row, col, time):
    total = flow * time
    cauldron = [0] * int(row * (row + 1) / 2)
    index = 0
    cauldron[index] = total

    for rows in range(1, row):
        for cols in range(1, rows + 1):
            total = cauldron[index]
            cauldron[index] = 100 if (total >= 100) else total
            total = (total - 100) if (total >= 100) else 0

            cauldron[index + rows] += total / 2
            cauldron[index + rows + 1] += total / 2
            index += 1

    return round(cauldron[int((row * (row - 1) / 2) + col - 1)], 2)

