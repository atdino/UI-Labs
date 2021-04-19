#!/usr/bin/python

import argparse

def configure_parser_and_get_args():
    parser = argparse.ArgumentParser(description='Laboratorijska vježba 2, UUUI, Ajdin Trejić')
    #had to do this because the lab instructions are weird✋
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

    exit(0)
    return result


def pl_resolution(F: set, G: str):
    clauses = set(F) # creates a set of clauses
    new_clauses = set()
    conclusion = None

    goal = negate_term(G)
    new_clauses.add(goal)

    
    while True:
        for [c1, c2] in select_clauses(clauses, new_clauses):
            resolvents = pl_resolve(c1, c2) #this should be a list since it requires a search

            if NIL in resolvents:
                conclusion = True
                break

            new_clauses.add(resolvents)

        if new_clauses.issubset(clauses):
            conclusion = False
            break

        clauses = clauses.add(new) 

def main():
    args = configure_parser_and_get_args()

    file_lines = load_file_lines(args.second_arg)

    F = set(file_lines[:-1])
    G = file_lines[-1]

    pl_resolution(F, G)

if __name__ == '__main__':
    main()
