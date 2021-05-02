#!/usr/bin/python

import argparse

def configure_parser_and_get_args():
    parser = argparse.ArgumentParser(description='Laboratorijska vježba 2, UUUI, Ajdin Trejić')
    parser.add_argument('list_args', type=str, nargs='*')
    return parser.parse_args()

def negate_term(term):
    if term[0] == '~':
        return term[1:]
    else:
        return '~' + term

def print_input(file_lines):
    #for i in range(len(file_lines) - 1):
        #print(str(i+1) + ". " +  file_lines[i])

    #This should be negated
    last_row = file_lines[-1]
    negated_last_row = negate_term(last_row)
    #print(str(len(file_lines)) + ". " +  negated_last_row)
    #print('#'*15)

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
    #print(clauses, new_clause)    
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
        print('[CONCLUSION]: ' + clause +' is unknown')

def is_tauntology(clause: str):
    clause_list = clause.split(' v ')
    for c in clause_list:
        if not is_negated(c) and negate_term(c) in clause_list:
            return True
    return False

def pl_resolve(c1: str, c2: str):
    result = None

    if is_tauntology(c1) or is_tauntology(c2):
        return result

    if len(c1) < len(c2):
        c1, c2 = c2, c1
    #print('pl_resolve: ', c1, ', ', c2)


    #if c2 is negative search for a positive in c1
    if not (' v ' in c1 and ' v ' in c2):
        if is_negated(c2) and (c2 + ' ' not in c1) and not c1.endswith(c2) and c1 != c2 and (c1.endswith(negate_term(c2)) or negate_term(c2) + ' ' in c1 ): #ovaj  2 uvjet je ako ima npr ~c i ~c da se ne vrati ~NIL
            non_negated = negate_term(c2)
            if non_negated in c1:
                
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
        elif (not is_negated(c2) and ('~' + c2 + ' ' in c1 or c1.endswith('~' + c2))):
            negated = negate_term(c2)
            if negated  in c1:
                
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
    elif (' v ' in c1 and ' v ' in c2):
        c1_list = c1.split(' v ')
        c2_list = c2.split(' v ')
        #print(c1_list)
        #print(c2_list)
    
        clauses_to_be_removed = []
        for clause_1 in c1_list:
            for clause_2 in c2_list:
                if clause_1 == negate_term(clause_2):
                    clauses_to_be_removed.append(clause_1)
                    clauses_to_be_removed.append(clause_2)
        if len(clauses_to_be_removed) == 0:
            result = None
        else:
            result_tmp = c1_list + c2_list
            result_list = []
            for c in result_tmp:
                if c not in clauses_to_be_removed:
                    result_list.append(c)
            if len(result_list) != 0:
                result = ' v '.join(result_list)
            else:
                result= None

    #print('pl_resolve returning: ', result)
    return result
def print_path(counter: int, found_by_dict: str):
    #for entry in found_by_dict:
    #    if entry[0] <= counter:
    #        continue
    #    print(str(entry[0]) + '. ' + str(entry[1]) + ' (' + str(entry[2]) + ', ' + str(entry[3]) + ')')
    length = len(found_by_dict)

    nil_entry = found_by_dict[-1]
    stack = []
    stack.append(nil_entry)
    
    result_list = []
    while stack:
        parent_element = stack.pop()
        if parent_element[2] == 0:
            continue
        child1_index = parent_element[2] - 1
        child2_index = parent_element[3] - 1
        
        stack.append(found_by_dict[child1_index])
        stack.append(found_by_dict[child2_index])
        entry= parent_element

        result_list.append((str(entry[0]) + '. ' + str(entry[1]) + ' (' + str(entry[2]) + ', ' + str(entry[3]) + ')'))

    result_list.reverse()

    for entry in result_list:
        print(entry)
def clear_redundant_clauses(clauses: set):
    to_remove = set()
    if len(clauses) == 0:
        return clauses
    else:
        for clause in clauses:
            for clause2 in clauses:
                if clause != clause2:
                    clause1_list= clause.split(' v ')
                    clause2_list= clause2.split(' v ')
                    if set(clause1_list).issubset(clause2_list):
                        to_remove.add(clause2)
                    if set(clause2_list).issubset(clause1_list):
                        to_remove.add(clause)
        for clause in clauses:
            if is_tauntology(clause):
                to_remove.add(clause)
    for c in to_remove:
        clauses.remove(c)
    return clauses
        


def pl_resolution(F: set, G: str):
    clauses = set(F) # creates a set of clauses
    new_clauses = set()
    conclusion = None
    found_by_dict = []

    counter = 0
    for clause in clauses:
        counter += 1
        print(str(counter) + '. ' + clause)
        found_by_dict.append([counter, clause, 0, 0])


    if ' v ' in G:
        goals = G.split(' v ')
        for goal in goals:
            new_clauses.add(negate_term(goal))
            #print(new_clauses)
            counter += 1
            print(str(counter) + '. ' + G)
            found_by_dict.append([counter, negate_term(goal), 0, 0])
        print('='*15)
    else:
        new_clauses.add(negate_term(G))
        counter += 1
        print(str(counter) + '. ' + negate_term(G))
        found_by_dict.append([counter, negate_term(G), 0, 0])
        print('='*15)


    original_counter = counter
    while new_clauses:
        new_clauses = clear_redundant_clauses(new_clauses)
        #print('#'*32)
        #print('for loop: clauses= ' + str(clauses) + ', new_clauses= ' + str(new_clauses))
        new_clause = new_clauses.pop()
        #print('new clause', new_clause)
        for [c1, c2] in select_clauses(clauses, new_clause):
            resolvents = pl_resolve(c1, c2) #this should be a list since it requires a search

            if resolvents != None and 'NIL' in resolvents:
                counter += 1

                c1_index = None
                c2_index = None

                for i in range(len(found_by_dict)):
                    if found_by_dict[i][1] == c1:
                        c1_index = i + 1
                    elif found_by_dict[i][1] == c2:
                        c2_index = i + 1
                
                found_by_dict.append([counter, resolvents, c1_index, c2_index])
                conclusion = True
                break
            if resolvents != None:
                #for resolvent in resolvents:
                #    new_clauses.add(resolvent)
                counter += 1

                c1_index = None
                c2_index = None

                for i in range(len(found_by_dict)):
                    if found_by_dict[i][1] == c1:
                        c1_index = i + 1
                    elif found_by_dict[i][1] == c2:
                        c2_index = i + 1
                
                found_by_dict.append([counter, resolvents, c1_index, c2_index])
                new_clauses.add(resolvents)
        if conclusion:
            break

        if new_clauses.issubset(clauses):
            conclusion = False
            break

        clauses.add(new_clause) 
    if conclusion:
        print_path(original_counter, found_by_dict)
    print_conclusion(conclusion, G)


def main():
    args = configure_parser_and_get_args()

    file_lines = load_file_lines(args.list_args[1])

    F = set(file_lines[:-1])
    G = file_lines[-1]
    if args.list_args[0] == 'resolution':
        pl_resolution(F, G)
    elif args.list_args[0] == 'cooking':
        F = set(file_lines)
        file_lines_input = load_file_lines(args.list_args[2])
        for command in file_lines_input:
            print('\nUser\'s command: ' + command)
            command_type = command[-1]
            command_sanitized = command[:-2]
            
            if command_type == '?':
                G = command_sanitized
                pl_resolution(F, G)
            elif command_type == '+':
                F.add(command_sanitized)
                print('Added ' + command_sanitized)
            elif command_type == '-':
                try:
                    F.remove(command_sanitized)
                    print('Removed ' + command_sanitized)
                except:
                    print('Cant remove ' + command_sanitized)
               

                
        #b dio zadatka
        #print('b zadatak')
        exit(0)

if __name__ == '__main__':
    main()
