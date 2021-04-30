#!/usr/bin/python

import argparse

def configure_parser_and_get_args():
    parser = argparse.ArgumentParser(description='Laboratorijska vježba 2, UUUI, Ajdin Trejić')
    parser.add_argument('first_arg', type=str)
    parser.add_argument('second_arg', type=str)
    return parser.parse_args()

def negate_term(term):
    if term[0] == '~':
        return term[1:]
    else:
        return '~' + term

def print_input(file_lines):
    for i in range(len(file_lines) - 1):
        print(str(i+1) + ". " +  file_lines[i])

    #This should be negated
    last_row = file_lines[-1]
    negated_last_row = negate_term(last_row)
    print(str(len(file_lines)) + ". " +  negated_last_row)
    print('#'*15)

#this function load a files lines in a arr
def load_file_lines(file_path):
    file_lines = []
    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            if line[0:1] != '#':
                    file_lines.append(line.lower())
    return file_lines


def select_clauses(clauses: set, new_clauses: set):
    #Uklanjanje redudantnih klauzula
    
    #Uklanjanje Nevazecih klauzula

    #Odaberi skup parova
    print(clauses, new_clauses)    
    result = set()
    for clause in clauses:
        for new_clause in new_clauses:
            result.add((clause, new_clause))
    return result

def is_negated(clause: str):
    if (clause[0] == '~'):
        return True
    else:
        return False

def is_tauntology(c1: str, c2:str):
    if ('~' + c1 == c2 or '~' + c2 == c1):
        return True
    else:
        return False

def pl_resolve(c1: str, c2: str):
    c1_list = c1.split()
    c2_list = c2.split()

    #remove or sign 
    while 'v' in c1_list: c1_list.remove('v')    
    while 'v' in c2_list: c2_list.remove('v')    


    clauses_to_be_resolved = c1_list + c2_list

    number_of_clauses = len(clauses_to_be_resolved)

    clauses_to_be_removed = []

    for i in range(number_of_clauses):
        for j in range(number_of_clauses):
            #print(clauses_to_be_resolved[i], clauses_to_be_resolved[j])
            if is_tauntology(clauses_to_be_resolved[i], clauses_to_be_resolved[j]):
                if clauses_to_be_resolved[i] not in clauses_to_be_removed:
                    clauses_to_be_removed.append(clauses_to_be_resolved[i])
                if clauses_to_be_resolved[j] not in clauses_to_be_removed:
                    clauses_to_be_removed.append(clauses_to_be_resolved[j])

    for clause in clauses_to_be_removed:
        if clause in clauses_to_be_resolved:
            clauses_to_be_resolved.remove(clause)
    #print(clauses_to_be_resolved)
    #print(clauses_to_be_removed)
    result = clauses_to_be_resolved
    return result

def pl_resolution(F: set, G: str):
    clauses = set(F) # creates a set of clauses
    new_clauses = set()
    conclusion = None

    goal = negate_term(G)

    new_clauses.add(goal)

    
    while True:
        print('#'*32)
        print('for loop: clauses= ' + str(clauses) + ', new_clauses= ' + str(new_clauses))
        for [c1, c2] in select_clauses(clauses, new_clauses):
            resolvents = pl_resolve(c1, c2) #this should be a list since it requires a search

            if 'NIL' in resolvents:
                conclusion = True
                break
            print(resolvents)


            for resolvent in resolvents:
                new_clauses.add(resolvent)

        if new_clauses.issubset(clauses):
            conclusion = False
            break

        clauses = clauses.add(new_clauses) 

def main():
    args = configure_parser_and_get_args()

    file_lines = load_file_lines(args.second_arg)

    F = set(file_lines[:-1])
    G = file_lines[-1]

    pl_resolution(F, G)

if __name__ == '__main__':
    main()
