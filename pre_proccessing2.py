import rmep

# Get the list needed by rmep.py, just glue the data column with class column.
# data_column: the data column
# class_column: the class label column
def get_discretization_data(data_column, class_column):
    size = len(data_column)
    result_list = []
    for i in range(size):
        result_list.append([data_column[i], class_column[i]])
    return result_list


# Replace numerical data with the No. of interval, i.e. consecutive positive integers.
# data: original data table
# column_no: the column No. of that column
# walls: the split point of the whole range
def replace_numerical(data, column_no, walls):
    size = len(data)
    num_spilt_point = len(walls)
    for i in range(size):
        if data[i][column_no] > walls[num_spilt_point - 1]:
            data[i][column_no] = num_spilt_point + 1
            continue
        for j in range(0, num_spilt_point):
            if data[i][column_no] <= walls[j]:
                data[i][column_no] = j + 1
                break
    return data

# Replace categorical values with a positive integer.
# data: original data table
# column_no: identify which column to be processed
def replace_categorical(data, column_no):
    size = len(data)
    classes = set([x[column_no] for x in data])
    classes_no = dict([(label, 0) for label in classes])
    j = 1
    for i in classes:
        classes_no[i] = j
        j += 1
    for i in range(size):
        data[i][column_no] = classes_no[data[i][column_no]]
    return data, classes_no

def discard(data, discard_list):
    size = len(data)
    length = len(data[0])
    data_result = []
    for i in range(size):
        data_result.append([])
        for j in range(length):
            if j not in discard_list:
                data_result[i].append(data[i][j])
    return data_result

# Main method here, see Description in detail
# data: original data table
# attribute: a list of the name of attribute
# value_type: a list identifying the type of each column
# Returned value: a data table after process
def pre_process(data, attribute, value_type):
    column_num = len(data[0])
    size = len(data)
    class_column = [x[-1] for x in data]
    discard_list = []
    for i in range(0, column_num - 1):
        data_column = [x[i] for x in data]
        # discretization
        if value_type[i] == "numerical":
            discretization_data = get_discretization_data(data_column, class_column)
            block = rmep.Block(discretization_data)
            walls = rmep.partition(block)
            if len(walls) == 0:
                max_value = max(data_column)
                min_value = min(data_column)
                step = (max_value - min_value) / 3
                walls.append(min_value + step)
                walls.append(min_value + 2 * step)
                # print out split points
            data = replace_numerical(data, i, walls)
        elif value_type[i] == "categorical":
            data, classes_no = replace_categorical(data, i)
            # print(attribute[i] + ":", classes_no)  # print out replacement list

        # discard
    if len(discard_list) > 0:
        data = discard(data, discard_list)
        print("discard:", discard_list)  # print out discard list
    return data


# just for test
if __name__ == "__main__":
    test_data = [
        ["red", 25.6, 56, 1],
        ["green", 33.3, 1, 1],
        ["green", 2.5, 23, 0],
        ["blue", 67.2, 111, 1],
        ["red", 29.0, 34, 0],
        ["yellow", 99.5, 78, 1],
        ["yellow", 10.2, 23, 1],
        ["yellow", 9.9, 30, 0],
        ["blue", 67.0, 47, 0],
        ["red", 41.8, 99, 1],
    ]
    test_attribute = ["color", "average", "age", "class"]
    test_value_type = ["categorical", "numerical", "numerical", "label"]
    test_data_after = pre_process(test_data, test_attribute, test_value_type)
    print(test_data_after)
