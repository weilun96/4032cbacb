import csv


# check if the var is float or int
def isNumeric(var):
    try:
        a = float(var)
        b = int(a)
        return True
    except (TypeError, ValueError):
        return False


def readData(datapath, namepath):
    data = []
    valueType = []
    with open(datapath, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            if len(line) == 1:
                line = line[0].split(" ")
            data.append(line)
        while [] in data:
            data.remove([])

    with open(namepath, "r") as file:
        headers = file.read()
        header = headers.split(",")

    # check whole column, if there are mixed numerical and strings then consider categorical
    for column in range(len(data[0])):
        numeric = set([isNumeric(x[column]) for x in data])
        if len(numeric) == 1:
            if True in numeric:
                valueType.append("numerical")
                for row in data:
                    row[column] = float(row[column])
            else:
                valueType.append("categorical")
        else:
            valueType.append("categorical")

    return header, data, valueType


def readExcel(path):
    header = []
    data = []
    valueType = []
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for line in reader:
            data.append(line)
        while [] in data:
            data.remove([])
    header.append(data[0])
    data.pop(0)

    # check whole column, if there are mixed numerical and strings then consider categorical
    for column in range(len(data[0])):
        numeric = set([isNumeric(x[column]) for x in data])
        if len(numeric) == 1:
            if True in numeric:
                valueType.append("numerical")
                for row in data:
                    row[column] = float(row[column])
            else:
                valueType.append("categorical")
        else:
            valueType.append("categorical")

    return header, data, valueType
