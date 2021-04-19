#!/usr/bin/python

import argparse
from queue import PriorityQueue
from queue import Queue

def configure_parser_and_get_args():
    parser = argparse.ArgumentParser(description='Laboratorijska vježba 1, UUUI, Ajdin Trejić')
    parser.add_argument('--alg', metavar='algorithm', required=False, type=str, help='algorithm type: bfs, ucs or astar')
    parser.add_argument('--ss', metavar='path', type=str, required=True, help='path')
    parser.add_argument('--h', metavar='path', type=str, help='heuristic path')
    parser.add_argument('--check-optimistic', action='store_true')
    parser.add_argument('--check-consistent', action='store_true')
    return parser.parse_args()


def print_result(alg_name, found_solution , states_visited, total_cost, path):
    print('# ' + alg_name)
    if found_solution:
        print('[FOUND_SOLUTION]: yes')
    else:
        print('[FOUND_SOLUTION]: no')
    print('[STATES_VISITED]: ' + str(states_visited))
    print('[PATH_LENGTH]: ' + str(len(path)))
    print('[TOTAL_COST]: ' + str(total_cost))
    print('[PATH]: ', end='')
    for i in range(len(path)-1):
        print(path[i] + " => ", end='')
    print(path[-1])


#this function load a files lines in a arr
def load_file_lines(file_path):
    file_lines = []
    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            if line[0:1] != '#':
                file_lines.append(line)
    return file_lines

def create_route_dict(file_lines):
    result = {}
    for line in file_lines:
        line = line.split(' ') # clean the trailing newline and make an array

        key = line[0][:-1]
        result[key] = {}
        node_entries = line[1:]
        for entry in node_entries:
            entry = entry.split(',')
            next_node = entry[0]
            next_node_distance = entry[1]
            result[key][next_node] = next_node_distance

    return result

def create_route_dict_heuristic(file_lines):
    result = {}
    for line in file_lines:
        line = line.split(' ') # clean the trailing newline and make an array
        key = line[0][:-1]
        result[key] = int(line[1])
    return result

def bfs(ss_path):
    ss_file_lines = load_file_lines(ss_path)
    start_node = ss_file_lines.pop(0) # returns the start node
    end_nodes = ss_file_lines.pop(0).split(' ') # returns the end node
    end_node = "" # this describes a node from end_nodes which was last hit
    ss_dict = create_route_dict(ss_file_lines)

    queue = Queue()
    enqueued = set()
    queue.put(start_node)

    visited = set()

    found_solution = False
    found_by_dict = {} # a dict which contains a k, v pair which linka a found node with the previous node which has found it

    while queue:
        #print('#'*10 + ' Queue: ' + str(list(queue.queue)))
        #print(' Visited: ' + str(visited))
        node = queue.get(0)
        if node in visited:
            continue
        visited.add(node)
        if node in end_nodes:
            found_solution = True
            end_node = node
            break

        #Get child nodes
        child_nodes = dict(ss_dict[node]) #this must be cast or it will override the ss_dict and mess stuff up
        while (len(child_nodes) != 0):

            closest_child_nodes = sorted(child_nodes)

            for closest_node in closest_child_nodes:
                if len(child_nodes) == 0: break
                #print(closest_node)
                child_nodes.pop(closest_node)

                if closest_node not in visited:
                    next_node = closest_node
                    if next_node not in enqueued:
                        found_by_dict[closest_node] = node
                        queue.put(next_node)
                        enqueued.add(next_node)

    #Trace a path back
    path = []
    cost = 0.0
    while True:
        if end_node == start_node:
            path.append(end_node)
            break
        layer_n = end_node
        layer_n_minus_1 = found_by_dict[layer_n]
        cost = cost + int(ss_dict[layer_n_minus_1][layer_n])
        path.append(layer_n)
        end_node = layer_n_minus_1
    path.reverse()

    print_result('BFS', found_solution, len(visited), cost, path)

def ucs(ss_path, start_node_given=""):
    ss_file_lines = load_file_lines(ss_path)
    
    if start_node_given == "":
        start_node = ss_file_lines.pop(0) # returns the start node
    else:
        ss_file_lines.pop(0)
        start_node = start_node_given
    end_nodes = ss_file_lines.pop(0).split(' ') # returns the end node
    end_node = "" # this describes a node from end_nodes which was last hit

    ss_dict = create_route_dict(ss_file_lines)

    queue = PriorityQueue()
    queue.put((0, start_node, ''))
    enqueued = set()
    enqueued.add(start_node)
    visited = set()

    found_solution = False
    found_by_dict = {} # a dict which contains a k, v pair which links a found node with the previous node which has found it

    while queue:
        #print( '\n' + '#'*10 + ' Queue: ' + str(list(queue.queue)))
        #print(' Visited: ' + str(visited))
        
        #find lowest distance node
        node = queue.get()

        if node[1] in visited:
            #print('skipping ' + node[1])
            continue
        else:
            found_by_dict[node[1]] = node[2]
            #print('visiting ' + node[1])


        visited.add(node[1])
        if node[1] in end_nodes:
            found_solution = True
            end_node = node[1]
            break

        #Get child nodes
        child_nodes = dict(ss_dict[node[1]]) #this must be cast or it will override the ss_dict and mess stuff up
        #print(child_nodes)

        for child_node in child_nodes:
            if child_node in visited: # if visited
                continue
            elif (child_node in enqueued): # if its already in queue but visited add it again
                new_dist = int(child_nodes[child_node]) + node[0]
                queue.put((new_dist, child_node, node[1]))
                #found_by_dict[child_node] = node[1]
            else:
                #found_by_dict[child_node] = node[1]
                distance = node[0] + int(child_nodes[child_node])
                queue.put((distance, child_node, node[1]))

    #Trace a path back
    path = []
    cost = 0.0
    while True:
        if end_node == start_node:
            path.append(end_node)
            break
        layer_n = end_node
        layer_n_minus_1 = found_by_dict[layer_n]
        cost = cost + int(ss_dict[layer_n_minus_1][layer_n])
        path.append(layer_n)
        end_node = layer_n_minus_1
    path.reverse()
    
    if not start_node_given == "":
        return cost

    print_result('UCS', found_solution, len(visited), cost, path)

def astar(ss_path, heuristic_path):
    ss_file_lines = load_file_lines(ss_path)
    heuristic_file_lines = load_file_lines(heuristic_path)

    start_node = ss_file_lines.pop(0) # returns the start node
    end_nodes = ss_file_lines.pop(0).split(' ') # returns the end node
    end_node = "" # this describes a node from end_nodes which was last hit

    ss_dict = create_route_dict(ss_file_lines)
    heuristic_dict = create_route_dict_heuristic(heuristic_file_lines)

    #print(heuristic_dict)

    queue = PriorityQueue()
    queue.put((0, start_node, '', 0)) 
    enqueued = set()
    enqueued.add(start_node)
    visited = set()

    found_solution = False
    found_by_dict = {} # a dict which contains a k, v pair which links a found node with the previous node which has found it
    while queue:
        #print( '\n' + '#'*10 + ' Queue: ' + str(list(queue.queue)))
        #print(' Visited: ' + str(visited))
        
        #find lowest distance node
        node = queue.get()

        if node[1] in visited:
            #print('skipping ' + node[1])
            continue
        else:
            found_by_dict[node[1]] = node[2]
            #print('visiting ' + node[1])


        visited.add(node[1])
        if node[1] in end_nodes:
            found_solution = True
            end_node = node[1]
            break

        #Get child nodes
        child_nodes = dict(ss_dict[node[1]]) #this must be cast or it will override the ss_dict and mess stuff up
        #print(child_nodes)

        for child_node in child_nodes:
            if child_node in visited: # if visited
                continue
            elif (child_node in enqueued): # if its already in queue but visited add it again
                approx_to_goal = int(heuristic_dict[child_node]) + node[3]
                new_dist = int(ss_dict[child_node])
                #print('from ' + node + ' to ' + child_node +' : ' + ss_dict)
                exit(0)
                queue.put((approx_to_goal , child_node, node[1], node[0]))
                #found_by_dict[child_node] = node[1]
            else:
                #new_dist = int(ss_dict[child_node])
                #print('from ' + str(node) + ' to ' + str(child_node) +' : ' + ss_dict[node[1]][child_node])
                #found_by_dict[child_node] = node[1]
                distance = node[3] + int(ss_dict[node[1]][child_node])
                approx_to_goal = int(heuristic_dict[child_node]) + distance
                queue.put((approx_to_goal, child_node, node[1], distance))

    #Trace a path back
    path = []
    cost = 0.0
    while True:
        if end_node == start_node:
            path.append(end_node)
            break
        layer_n = end_node
        layer_n_minus_1 = found_by_dict[layer_n]
        cost = cost + int(ss_dict[layer_n_minus_1][layer_n])
        path.append(layer_n)
        end_node = layer_n_minus_1
    path.reverse()

    print_result('A-STAR ' + heuristic_path, found_solution, len(visited), cost, path)

def print_optimistic_condition(node, heuristic_dist, real_dist):
    heuristic_dist = 0.0 + heuristic_dist 
    data_to_print = []
    data_to_print.append('[CONDITION]:')
    if heuristic_dist > real_dist:
        data_to_print.append('[ERR]')
    else:
        data_to_print.append('[OK]')
    data_to_print.append('h(' + node + ')')
    data_to_print.append('<=')
    data_to_print.append('h*:')
    data_to_print.append(str(heuristic_dist))
    data_to_print.append('<=')
    data_to_print.append(str(real_dist))
    print(' '.join(data_to_print))

def print_consistent_condition(heuristic_1, heuristic_2, distance, node, child_node):
    heuristic_1 = 0.0 + heuristic_1
    heuristic_2 = 0.0 + heuristic_2
    distance = float(distance)
    data_to_print = []
    data_to_print.append('[CONDITION]:')
    if heuristic_1 > heuristic_2 + distance:
        data_to_print.append('[ERR]')
    else:
        data_to_print.append('[OK]')
    data_to_print.append('h(' + node + ')')
    data_to_print.append('<=')
    data_to_print.append('h(' + child_node + ')')
    data_to_print.append('+ c:')
    data_to_print.append(str(heuristic_1))
    data_to_print.append('<=')
    data_to_print.append(str(heuristic_2))
    data_to_print.append('+')
    data_to_print.append(str(distance))
    print(' '.join(data_to_print))

def check_optimistic(ss_path, heuristic_path):
    print("# HEURISTIC-OPTIMISTIC " + heuristic_path)
    ss_file_lines = load_file_lines(ss_path)
    heuristic_file_lines = load_file_lines(heuristic_path)
    heuristic_dict = create_route_dict_heuristic(heuristic_file_lines)


    uniq_nodes = PriorityQueue()
    for line in heuristic_file_lines:
        uniq_nodes.put(line.split(' ')[0][:-1])
    failed = False
    while not uniq_nodes.empty():
        node = uniq_nodes.get()
        distance = ucs(ss_path, node)
        heuristic_distance = heuristic_dict[node]
        if heuristic_distance > distance:
            failed = True
        print_optimistic_condition(node, heuristic_distance,  distance)
    if failed:
        print('[CONCLUSION]: Heuristic is not optimistic.')
    else:
        print('[CONCLUSION]: Heuristic is optimistic.')

def check_consistent(ss_path, heuristic_path):
    print("# HEURISTIC-CONSISTENT " + heuristic_path)
    ss_file_lines = load_file_lines(ss_path)
    heuristic_file_lines = load_file_lines(heuristic_path)
    ss_file_lines.pop(0)
    ss_file_lines.pop(0)
    ss_dict = create_route_dict(ss_file_lines)
    heuristic_dict = create_route_dict_heuristic(heuristic_file_lines)

    uniq_nodes = PriorityQueue()

    for line in heuristic_file_lines:
        uniq_nodes.put(line.split(' ')[0][:-1])
    failed = False

    while not uniq_nodes.empty():
        node = uniq_nodes.get()

        child_nodes = list(ss_dict[node].keys())
        child_nodes = sorted(child_nodes)
        for child_node in child_nodes:
            if heuristic_dict[node] > heuristic_dict[child_node] + float(ss_dict[node][child_node]):
                failed = True

            print_consistent_condition(heuristic_dict[node], heuristic_dict[child_node], ss_dict[node][child_node], node, child_node)

    if failed:
        print('[CONCLUSION]: Heuristic is not consistent.')
    else:
        print('[CONCLUSION]: Heuristic is consistent.')
    

def main():
    args = configure_parser_and_get_args()

    if (args.alg == 'bfs'):
        bfs(args.ss)
    elif (args.alg == 'ucs'):
        ucs(args.ss)
    elif (args.alg == 'astar'):
        astar(args.ss, args.h)
    elif (args.check_optimistic == True):
        check_optimistic(args.ss, args.h)
    elif (args.check_consistent == True):
        check_consistent(args.ss, args.h)

if __name__ == '__main__':
    main()

