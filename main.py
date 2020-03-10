import re
import math


def in_file():
    with open("input_1.txt", 'r') as f:
        matrix = [[sign for sign in re.sub(',|\n', '', line)] for line in f]
    return matrix


def test_file():
    with open("input_2.txt", 'r') as f:
        test_data = [[sign for sign in re.sub(',|\n', '', line)] for line in f]
    return test_data


def get_attr(matrix):
    attribute = []
    for counter in range(23):
        num_of_attr = 0
        attr_array = []
        for iterator in range(len(matrix)):
            if matrix[iterator][counter] not in attr_array:
                attr_array.append(matrix[iterator][counter])
                num_of_attr += 1
        attribute.append([counter, 0, num_of_attr, attr_array])
    return attribute


def is_leaf(matrix):
    if not matrix:
        return 3  # doesn't exists
    edible = False
    poisonous = False
    for mushroom in range(len(matrix)):
        if matrix[mushroom][0] == 'p':
            poisonous = True
        if matrix[mushroom][0] == 'e':
            edible = True
    if (edible == True and poisonous == True):
        return 0    # not leaf
    elif edible == True:
        return 1    # edible leaf
    elif poisonous == True:
        return 2    # poisonous leaf


def inf_gain(matrix, attribute):
    max_gain = 0
    index = 0
    ent = entropy(matrix)
    for count in range(22):
        attr_num = count+1
        if attribute[attr_num][1] == 1:
            continue
        gain = ent - attr_entropy(matrix, attribute, attr_num)
        if (gain == max_gain):
            if(attribute[attr_num][2] < attribute[index][2]):
                index = attr_num
        if (gain > max_gain):
            max_gain = gain
            index = attr_num
    return index


def entropy(matrix):
    pos = 0
    ent = 0
    for iterator in range(len(matrix)):
        if (matrix[iterator][0] == 'e'):
            pos += 1
    p = pos/len(matrix)
    if (p > 0 and p < 1):
        ent = ((-1) * p * math.log(p, 2))
        p = 1-p
        ent -= (p * math.log(p, 2))
    return ent


def attr_entropy(matrix, attribute, attr_num):
    num_of_attr = attribute[attr_num][2]
    val = attribute[attr_num][3]
    ent = 0
    for it in range(num_of_attr):
        pos = 0
        total = 0
        for iterator in range(len(matrix)):
            if (matrix[iterator][attr_num] == val[it]):
                total += 1
                if (matrix[iterator][0] == 'e'):
                    pos += 1
        if total > 0:
            p = pos/total
        else:
            p = 0
        if (p > 0) and (p < 1):
            score = (-1)*(p * math.log(p, 2))
            p = 1-p
            score -= (p*math.log(p, 2))
            score = score*total/len(matrix)
            ent += score
    return ent


def find_place(nodes_list, result):
    for counter_out in range(len(nodes_list)):
        for counter_in in range(len(nodes_list[counter_out][3])):
            if nodes_list[counter_out][3][counter_in] == 0:
                nodes_list[counter_out][3][counter_in] = result
                return nodes_list


def split_tree(matrix, temp_matrix, attr_num):
    num_of_attr = 0
    val_array = []
    for counter in range(len(matrix)):
        if matrix[counter][attr_num] not in val_array:
            val_array.append(matrix[counter][attr_num])
    for val in range(len(val_array)):
        sub_temp_matrix = []
        for counter in range(len(matrix)):
            if (val_array[val] == matrix[counter][attr_num]):
                sub_temp_matrix.append(matrix[counter])
        temp_matrix.append(sub_temp_matrix)
    return temp_matrix


def create_node(matrix, attribute):
    if is_leaf(matrix) == 1:
        return 'e', 0
    if is_leaf(matrix) == 2:
        return 'p', 0
    if is_leaf(matrix) == 3:
        return '!', 0
    attr_num = inf_gain(matrix, attribute)
    attribute[attr_num][1] = 1  # flag
    temp_matrix = []
    temp_matrix = split_tree(matrix, temp_matrix, attr_num)
    return attr_num, temp_matrix


def start_ID3(matrix, attribute, nodes_list, ancestor):
    if not matrix:
        print("File with date is empty")
        return
    result, temp_matrix = create_node(matrix, attribute)
    if (result == 'p' or result == 'e' or result == '!'):
        return find_place(nodes_list, result)
    else:
        node_list = find_place(nodes_list, result)
    list_of_branches = []
    for counter in attribute[result][3]:
        list_of_branches.append(0)
    nodes_list.append(
        [result, ancestor, [attribute[result][3]], list_of_branches])
    ancestor = result

    for iterator in range(len(temp_matrix)):
        nodes_list = (
            start_ID3(temp_matrix[iterator], attribute, nodes_list, ancestor))
    return nodes_list


def classify(data, nodes_list):
    iterator = 0
    up = 0
    attr_num = nodes_list[0][0]
    for counter in range(len(nodes_list)):
        if (attr_num == nodes_list[counter][0]):
            data_val = data[attr_num]
            for val in range(len(nodes_list[counter][2])):
                if(nodes_list[counter][2][0][val] == data_val):
                    iterator = data_val
                    if(iterator == 'p' or iterator == 'e'):
                        up = 1
                        return 1
                    else:
                        attr_num = iterator
    return 0


def test(nodes_list, result_array):
    test_data = test_file()
    counter = 0
    if not test_data:
        print("File with date is empty")
        return
    for i in range(len(test_data)):
        counter += classify(test_data[i], nodes_list)
    return counter, len(test_data)


def main():
    first_ancestor = 0
    matrix = in_file()
    attribute = get_attr(matrix)
    print(attribute)
    nodes_list = []
    nodes_list = start_ID3(matrix, attribute, nodes_list, first_ancestor)
    print(nodes_list)
    result_array = []
    test(nodes_list, result_array)
    print(attribute)
    #print(test(nodes_list, result_array))


main()
