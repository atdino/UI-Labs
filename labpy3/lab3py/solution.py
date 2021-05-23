#!/usr/bin/python

import argparse
import math
import copy

tree = dict()
result = ''

def configure_parser_and_get_args():
    parser = argparse.ArgumentParser(description='Laboratorijska vježba 3, UUUI, Ajdin Trejić')
    parser.add_argument('list_args', type=str, nargs='*')
    return parser.parse_args()

def load_file_lines(file_path):
    file_lines = []
    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            file_lines.append(line.split(','))
    return file_lines

def get_entropy(data: dict):
    """
    funtion requires a data of type dict, e.g. data = {'no': 5, 'yes': 9}
    """

    #calculating probability
    total_occurances = sum(list(data.values()))
    probabilties_of_outcomes = list()
    for key in data.keys():
        occurances_by_outcome = data[key]
        probability_of_occurance = occurances_by_outcome/total_occurances
        probabilties_of_outcomes.append(probability_of_occurance)

    #calculating entropy
    entropy = 0
    for probability in probabilties_of_outcomes:
        entropy += -1 * probability * math.log(probability, 2) # base is 2

    return entropy

def get_starting_entropy(data: list):
    outcomes = list() # contains a list of outcomes, if multiple outcomes occur, only 1 is stored, i could have used a set but sets aren't ordered
    for entry in data:
        outcome = entry[-1]
        if outcome not in outcomes:
            outcomes.append(outcome)

    times_outcome_happend = dict()
    for entry in data:
        outcome = entry[-1]
        if outcome not in times_outcome_happend:
            times_outcome_happend[outcome] = 1
        else:
            times_outcome_happend[outcome] += 1
    
    entropy = get_entropy(times_outcome_happend)
    return entropy

def filter_data(data: list, attribute_index: int, filter_value: str):
    """
    Function takes lines of data and filters out specific values, e.g. D(weather) = sunny
    """

    filtered_data = list()
    for entry in data:
        if entry[attribute_index] == filter_value:
            filtered_data.append(list(entry)) # this needs to be copied to a new list or python will pass it by reference

    for i in range(len(filtered_data)):
        filtered_data[i].pop(attribute_index)

    return filtered_data

def get_information_gain(data: list, attribute_index: int):
    #print('getting information gain: ', attribute_index)
    #print('\n\n')
    #print(*data, sep='\n')
    #print('\n\n')
    starting_entropy = get_starting_entropy(data)

    total_occurances = len(data)
    total_occurances_by_value = dict()

    #get all possible values
    possible_values = list()
    entropy_dict = dict()
    for entry in data:
        possible_values.append(entry[attribute_index])

    possible_values = list(dict.fromkeys(possible_values)) # remove duplicates
    
    for possible_value in possible_values:
        #to find entropy for specific attribute value i have to construct data required by get_entropy function
        data_to_calc_entropy = list()
        for entry in data:
            if entry[attribute_index] == possible_value:
                data_to_calc_entropy.append(entry[-1])
                if possible_value not in total_occurances_by_value:
                    total_occurances_by_value[possible_value] = 1
                else:
                     total_occurances_by_value[possible_value] += 1


        #put it in a dict to match the expected data for get_entropy
        data_as_dict = dict()
        for value in data_to_calc_entropy:
            if value not in data_as_dict:
                data_as_dict[value] = 1
            else:
                data_as_dict[value] += 1
        #print('--->data_as_dict:', data_as_dict)
        attribute_entropy = get_entropy(data_as_dict)
        #print('----->attribute_entropy:', attribute_entropy)
        entropy_dict[possible_value] = attribute_entropy
    information_gain = 0
    information_gain += starting_entropy
    for key in entropy_dict.keys():
        information_gain -= entropy_dict[key] * total_occurances_by_value[key] / total_occurances
    
    #print('-------->information_gain:', information_gain)
    return information_gain, entropy_dict
    

def get_average_information():
    entropy = get_entropy()
    information_gain = get_information_gain()
    gain = entropy - information_gain
    return gain

class Model:
    test = 'test'

    def __init__(self):
        self.test='test2'

    def fit():
        test='test'

    def predict():
        test='test'

def id3(data: list, data_parent: list, attributes: list, y: str, z: str, depth:int):
    print('\n\n#### ID3',  attributes, y, z, depth)
    global tree

    if y == 'D':
        print(data)

    if depth != -2:
        depth =  depth - 1
    
    
    #if its empty take the most probable outcome from the original data
    if not data_parent or depth == -1: 
        outcomes = dict()
        for entry in data_parent:
            outcome = entry[-1]
            if outcome not in outcomes:
                outcomes[outcome] = 1
            else:
                outcomes[outcome] += 1
        return_data = dict()
        return_data['node'] = max(outcomes, key=outcomes.get)
        return return_data # leaf

    #if all outcomes are the same
    comparator = data[0][-1]
    done = True
    for i in range(len(data)):
        if comparator != data[i][-1]:
            done = False

    if done:
        return_data = dict()
        return_data['node'] = comparator
        print(return_data, y, z)
        return return_data

    if len(attributes) == 1:
        outcomes = dict()
        for entry in data:
            outcome = entry[-1]
            if outcome not in outcomes:
                outcomes[outcome] = 1
            else:
                outcomes[outcome] += 1
        return_data = dict()
        return_data['node'] = attributes[0]
        return_data['paths'] = dict()
        for line in data:
            k, v = line[0], line[-1]
            #print(k, v)
            return_data['paths'][k] = v
        if y == 'D':
            print('data', data)
            print('return_data paths', return_data['paths'])
            exit(0)
        return  return_data


    information_gain_dict = dict()
    for i in range(len(attributes)):
        attribute_index = i
        information_gain, entropy_dict = get_information_gain(data, attribute_index)
        information_gain_dict[attributes[attribute_index]] = {'information_gain': information_gain, 'entropy_dict': entropy_dict}

    for node in information_gain_dict.keys():
        print('IG(%s)=%.4f ' % (node, information_gain_dict[node]['information_gain']), end='')
    print()
    max_information_gain = -1
    max_information_key = ''
    for attribute in information_gain_dict.keys():
        if information_gain_dict[attribute]['information_gain'] > max_information_gain:
            max_information_key = attribute
            max_information_gain = information_gain_dict[attribute]['information_gain']
            
    #if max information gain is 0 then all atributes are the same,

    max_information_index = attributes.index(max_information_key)
    attributes.pop(max_information_index)
    subtrees = list()
    for child_attribute in information_gain_dict[max_information_key]['entropy_dict'].keys():
        new_data = filter_data(copy.deepcopy(data), max_information_index, child_attribute)

        result_raw = id3(copy.deepcopy(new_data), copy.deepcopy(data), list(attributes), max_information_key, child_attribute, depth)
        result = result_raw['node']
        
        #if 'paths' in result_raw:
        #    #print('tree', tree)
        #    #print('result_raw[\'paths\']', result_raw['paths'])
        #    if result_raw['node'] == 'D':
        #        print(result_raw)
        #        print('banana')
        #        if str(result_raw) != "{'node': 'D', 'paths': {'True': 'True', 'False': 'False'}}":
        #            exit(0)
        #    if result_raw['node'] not in tree:
        #        tree[result_raw['node']] = dict()
        #    tree[result_raw['node']].update(result_raw['paths'])

        if 'paths' in result_raw:
            if result_raw['node'] not in tree:
                tree[result_raw['node']] = dict()
                tree[result_raw['node']] = result_raw['paths']
        
        subtrees.append(child_attribute + ' -> ' + result)
    #print(max_information_key, subtrees)
    return_data = dict()
    return_data['node'] = max_information_key
    return_data['paths'] = dict()
    for subtree in subtrees:
        k, v = subtree.split(' -> ')
        return_data['paths'][k] = v
    return return_data
    
#kopirao sam ovih 7 linija ispod sa stackoverflowa, sluzi mi cisto za debugging
def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))

def pretty_autograder(d: dict, r: str, c: int, prefix:str):
    #print(d, r, c)
    for k, v in d[r].items():
        output = prefix + str(c) + ':' + r + '=' + k +' '
        if v in d.keys():
            pretty_autograder(d, v, c+1, output)
        else:
            print(output, end='')
            print(v, end='')
            print()

def test_prediction(line: list, tree:dict, root: str, attributes: list):
    global result
    result += ' ' 
    #print('\nTesting prediction:', end=', ')
    #print('line: ' + str(line), end=', ')
    #print('tree: ' + str(tree), end=', ')
    #print('atr: ' + str(attributes), end=', ')
    #print('root: ' + str(root))

    def recursive_prediction(p: str, line: list):
        global result
        #print('recc: ', p, line)
        atr_index = attributes.index(p)
        atr_value = line[atr_index]
        #print('indx: ', atr_index)
        #print('val: ', atr_value)
        next = tree[p][atr_value]
        if next in tree.keys():
            recursive_prediction(next, line)
        else:
            result += next

    recursive_prediction(root, line)
    #print('attributes: ' + str(attributes))
    

def main():
    global result
    args = configure_parser_and_get_args()
    file_lines = load_file_lines(args.list_args[0])

    try:
        depth = int(args.list_args[2]) + 1
    except:
        depth = -2
    depth = -2
    attributes = file_lines[0][:-1] # -1 is to cut off the last element (outcome)
    #print('attributes: ' + str(attributes))
    data = file_lines[1:]

    result_raw = id3(data, data, list(attributes), 'ROOT', 'ROOT', depth) # start the algorithm

    if 'paths' in result_raw: # this is required only for adding the root node to the tree
        tree[result_raw['node']] = result_raw['paths']

    root = result_raw['node']
	 
    pretty(tree)
    print(tree)
    print('[BRANCHES]:')
    pretty_autograder(tree, root, 1, '')


    test_file_lines = load_file_lines(args.list_args[1])[1:]
    print('[PREDICTIONS]:', end='')

    for line in test_file_lines:
        test_prediction(copy.deepcopy(line), tree, root, attributes)
    
   
    test_true_results = list()
    for line in test_file_lines:
        test_true_results.append(line[-1])
    
    print(result)
    result = result.split()
    #print(result)
    #print(test_true_results)
    
    accurate = 0
    for i in range(len(result)):
        if result[i] == test_true_results[i]:
            accurate += 1

    print('[ACCURACY]: %.5f' % (accurate/len(result)))


    print('[CONFUSION_MATRIX]:')
    size = len(set(result + test_true_results))
    matrix = [[0 for x in range(size)] for y in range(size)] 

    outputs = list(set(result + test_true_results))
    outputs.sort()
    for i in range(len(result)):
        if result[i] == test_true_results[i]:
            j = outputs.index(result[i])
            matrix[j][j] += 1
        if result[i] != test_true_results[i]:
            j = outputs.index(result[i])
            k = outputs.index(test_true_results[i])
            matrix[k][j] += 1
    
    for row in matrix:
        print(*row, sep=' ')


if __name__ == '__main__':
    main()
