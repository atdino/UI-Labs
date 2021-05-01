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


def select_clauses(clauses: set, new_clause: str):
    #Uklanjanje redudantnih klauzula
    
    #Uklanjanje Nevazecih klauzula

    #Odaberi skup parova
    print(clauses, new_clause)    
    result = set()
    for clause in clauses:
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

def print_conclusion(conclusion: bool, clause: str):
    if conclusion:
        print('[CONCLUSION]: ' + clause +' is true')
    else:
        print('[CONCLUSION]: ' + clause +' is false')

def pl_resolve(c1: str, c2: str):
    result = None 

    if len(c1) < len(c2):
        c1, c2 = c2, c1
    print('pl_resolve: ', c1, ', ', c2)

    #if c2 is negative search for a positive in c1
    if is_negated(c2) and ' ' + c2 + ' ' not in c1: #ovaj  2 uvjet je ako ima npr ~c i ~c da se ne vrati ~NIL
        non_negated = negate_term(c2)
        if ' ' + non_negated + ' ' in c1:
            
            placement_check_1 = ' v ' + non_negated + ' v '
            placement_check_2 = ' v ' + non_negated
            placement_check_3 = non_negated + ' v '
            placement_check_4 = non_negated

            if placement_check_1 in c1:
                result = c1.replace(placement_check_1, ' v ')
            elif placement_check_2 in c1:
                result = c1.replace(placement_check_2, '')
            elif placement_check_3 in c1:
                result = c1.replace(placement_check_3, '')
            elif placement_check_4 in c1:
                result = c1.replace(placement_check_4, 'NIL')
    #if c2 is positive search for a negative in c1
    elif (not is_negated(c2) and ' ~' + c2 + ' ' in c1):
        negated = negate_term(c2)
        if negated in c1:
            
            placement_check_1 = ' v ' + negated + ' v '
            placement_check_2 = ' v ' + negated
            placement_check_3 = negated + ' v '
            placement_check_4 = negated

            if placement_check_1 in c1:
                result = c1.replace(placement_check_1, ' v ')
            elif placement_check_2 in c1:
                result = c1.replace(placement_check_2, '')
            elif placement_check_3 in c1:
                result = c1.replace(placement_check_3, '')
            elif placement_check_4 in c1:
                result = c1.replace(placement_check_4, 'NIL')


    print('pl_resolve returning: ', result)
    return result
    


def pl_resolution(F: set, G: str):
    clauses = set(F) # creates a set of clauses
    new_clauses = set()
    conclusion = None

    goal = negate_term(G)

    new_clauses.add(goal)

    
    while new_clauses:
        print('#'*32)
        print('for loop: clauses= ' + str(clauses) + ', new_clauses= ' + str(new_clauses))
        new_clause = new_clauses.pop()
        print('new clause', new_clause)
        for [c1, c2] in select_clauses(clauses, new_clause):
            resolvents = pl_resolve(c1, c2) #this should be a list since it requires a search

            if resolvents != None and 'NIL' in resolvents:
                conclusion = True
                break
            if resolvents != None:
                #for resolvent in resolvents:
                #    new_clauses.add(resolvent)
                new_clauses.add(resolvents)
        if conclusion:
            break

        if new_clauses.issubset(clauses):
            conclusion = False
            break

        clauses.add(new_clause) 
    
    print_conclusion(conclusion, G)
def main():
    args = configure_parser_and_get_args()

    file_lines = load_file_lines(args.second_arg)

    F = set(file_lines[:-1])
    G = file_lines[-1]

    pl_resolution(F, G)

if __name__ == '__main__':
    main()
